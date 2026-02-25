"""Tests for ConcurrentStorage memory leak fix (PR #526)."""
import gc
import weakref

import pytest

from framework.storage.concurrent import ConcurrentStorage


@pytest.fixture
def storage(tmp_path):
    # Determine the directory path
    base_path = tmp_path / "storage"
    # Return initialized storage with small max_locks for easier testing
    return ConcurrentStorage(base_path=base_path, max_locks=10)

@pytest.mark.asyncio
async def test_lock_lifecycle(storage):
    """Test that locks are created and managed correctly."""
    await storage.start()

    # Access a lock
    lock1 = await storage._get_lock("run:123")
    assert lock1 is not None

    # Access same lock again - should be identical object
    lock2 = await storage._get_lock("run:123")
    assert lock1 is lock2

    # Check internal state
    assert "run:123" in storage._file_locks
    assert "run:123" in storage._lru_tracking

    await storage.stop()

@pytest.mark.asyncio
async def test_lru_eviction(storage):
    """Test that LRU mechanism evicts old locks from strong reference tracking."""
    # storage has max_locks=10

    # Create 15 locks (more than max_locks)
    locks = []
    for i in range(15):
        locks.append(await storage._get_lock(f"run:{i}"))

    # Check that we only track 10 strong refs
    assert len(storage._lru_tracking) <= 10

    # The most recent ones (14, 13...) should be tracked
    assert "run:14" in storage._lru_tracking

    # The oldest ones (0, 1...) should have been evicted from LRU
    # Note: They might still be in _file_locks because 'locks' list holds a ref
    assert "run:0" not in storage._lru_tracking

@pytest.mark.asyncio
async def test_weak_ref_garbage_collection(storage):
    """Test that evicted locks are actually garbage collected when no longer used."""

    # Create a lock
    lock = await storage._get_lock("run:temp")

    # Create a weak ref to observe it
    weak_lock = weakref.ref(lock)

    # Force eviction by adding more locks
    for i in range(20):
        await storage._get_lock(f"run:{i}")

    # Verify it's gone from LRU
    assert "run:temp" not in storage._lru_tracking

    # Drop our hard reference
    del lock

    # Force GC
    gc.collect()

    # The lock should now be dead
    # Note: This might be flaky depending on python implementation details,
    # but with WeakValueDictionary it should disappear from _file_locks
    assert weak_lock() is None or "run:temp" not in storage._file_locks

@pytest.mark.asyncio
async def test_index_locks_are_weak(storage):
    """Test that index locks are NOT kept in LRU (strong refs)."""

    _ = await storage._get_lock("index:by_status:completed")

    # Should be in file_locks (weak dict)
    assert "index:by_status:completed" in storage._file_locks

    # Should NOT be in LRU tracking (strong dict)
    assert "index:by_status:completed" not in storage._lru_tracking
