import 'package:flutter/foundation.dart';
import '../models/session_event.dart';

/// SessionTracker — ChangeNotifier that records every card interaction.
/// Used by GameScreen to build the event list sent to AntigravityService every 30s.
/// Used by ParentDashboard and AntigravityService to build session summaries.
class SessionTracker extends ChangeNotifier {
  // ─── CHILD PROFILE ──────────────────────────────────────────────
  String _childId = 'child_001';
  String _childName = 'Zara';

  String get childId => _childId;
  String get childName => _childName;

  void setChildProfile({required String id, required String name}) {
    _childId = id;
    _childName = name;
    notifyListeners();
  }

  // ─── SESSION STATE ───────────────────────────────────────────────
  static const int _maxEvents = 500;
  final List<SessionEvent> _events = [];
  DateTime? _sessionStart;
  String _currentCategory = 'animals';
  int _totalSuccesses = 0;
  int _totalAttempts = 0;

  // ─── RETENTION TRACKING ─────────────────────────────────────────
  DateTime? _lastDifficultyIncrease;

  List<SessionEvent> get allEvents => List.unmodifiable(_events);
  String get currentCategory => _currentCategory;
  int get totalSuccesses => _totalSuccesses;
  int get totalAttempts => _totalAttempts;
  double get overallSuccessRate =>
      _totalAttempts == 0 ? 0 : _totalSuccesses / _totalAttempts;

  double get sessionDurationMins {
    if (_sessionStart == null) return 0;
    return DateTime.now().difference(_sessionStart!).inSeconds / 60.0;
  }

  // ─── RECORDING ──────────────────────────────────────────────────

  /// Record a card tap event. Called by GameScreen on every tap.
  void recordEvent({
    required String cardId,
    required String category,
    required bool isSuccess,
    double tapSpeed = 1.0,
    int tapCount = 1,
  }) {
    _sessionStart ??= DateTime.now();
    _currentCategory = category;
    _totalAttempts++;
    if (isSuccess) _totalSuccesses++;

    _events.add(SessionEvent(
      childId: _childId,
      eventType: isSuccess ? 'card_success' : 'card_fail',
      cardId: cardId,
      category: category,
      timestamp: DateTime.now(),
      isSuccess: isSuccess,
      tapSpeed: tapSpeed,
      tapCount: tapCount,
    ));

    if (_events.length > _maxEvents) _events.removeAt(0);

    notifyListeners();
  }

  /// Returns events from the last [seconds] seconds — used by the 30s agent check.
  List<SessionEvent> getRecentEvents({int seconds = 60}) {
    final cutoff = DateTime.now().subtract(Duration(seconds: seconds));
    return _events.where((e) => e.timestamp.isAfter(cutoff)).toList();
  }

  /// Count consecutive failures from the end of the event list.
  int get consecutiveFailures {
    int count = 0;
    for (final e in _events.reversed) {
      if (!e.isSuccess) {
        count++;
      } else {
        break;
      }
    }
    return count;
  }

  /// Average tap speed over recent events (frustration proxy).
  double get recentTapSpeed {
    final recent = getRecentEvents(seconds: 30);
    if (recent.isEmpty) return 0;
    return recent.map((e) => e.tapSpeed).reduce((a, b) => a + b) / recent.length;
  }

  // ─── RETENTION METRICS ──────────────────────────────────────────

  /// Fraction of attempts that were failures (retry rate).
  double get retryRate =>
      _totalAttempts == 0 ? 0.0 : (_totalAttempts - _totalSuccesses) / _totalAttempts;

  /// True when session is long but success rate is low — churn risk signal.
  bool get isChurnRisk =>
      sessionDurationMins > 10 && overallSuccessRate < 0.4;

  /// Called by GameScreen when a difficulty-increase adaptation is applied.
  void recordDifficultyIncrease() {
    _lastDifficultyIncrease = DateTime.now();
  }

  /// True when difficulty was increased recently but no taps followed within 30s.
  bool get hasDifficultySpikeAbandonment {
    if (_lastDifficultyIncrease == null) return false;
    final sinceIncrease =
        DateTime.now().difference(_lastDifficultyIncrease!).inSeconds;
    if (sinceIncrease > 120) return false; // window expired — clear signal
    final lastEventTime =
        _events.isEmpty ? _lastDifficultyIncrease! : _events.last.timestamp;
    return DateTime.now().difference(lastEventTime).inSeconds > 30;
  }

  // ─── SESSION LIFECYCLE ───────────────────────────────────────────

  /// Call when onboarding completes or when switching children.
  void startNewSession({String? childId, String? childName}) {
    if (childId != null) _childId = childId;
    if (childName != null) _childName = childName;
    _events.clear();
    _sessionStart = DateTime.now();
    _totalSuccesses = 0;
    _totalAttempts = 0;
    _currentCategory = 'animals';
    _lastDifficultyIncrease = null;
    notifyListeners();
  }

  /// Build a summary map for the weekly report endpoint.
  Map<String, dynamic> buildWeekSummary() {
    return {
      'total_attempts': _totalAttempts,
      'total_successes': _totalSuccesses,
      'success_rate': overallSuccessRate,
      'session_duration_mins': sessionDurationMins,
      'current_category': _currentCategory,
      'consecutive_failures': consecutiveFailures,
    };
  }
}
