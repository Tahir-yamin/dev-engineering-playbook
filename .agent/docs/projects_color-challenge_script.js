// Chromatic Symphony - 3D Color Particle Universe
// February 2026 CodePen Challenge - Color Palettes

// ==================== PALETTE CONFIGURATION ====================
const PALETTE = [
    { name: 'Neon Coral', hex: '#FF6B9D', rgb: [1.0, 0.42, 0.62] },
    { name: 'Electric Cyan', hex: '#00D9FF', rgb: [0.0, 0.85, 1.0] },
    { name: 'Violet Pulse', hex: '#C77DFF', rgb: [0.78, 0.49, 1.0] },
    { name: 'Lime Burst', hex: '#39FF14', rgb: [0.22, 1.0, 0.08] },
    { name: 'Solar Gold', hex: '#FFD60A', rgb: [1.0, 0.84, 0.04] },
    { name: 'Ruby Glow', hex: '#FF006E', rgb: [1.0, 0.0, 0.43] }
];

// ==================== SCENE SETUP ====================
let scene, camera, renderer, particles = [];
let mode = 'orbit';
let mouseX = 0, mouseY = 0, mouseZ = 0;
let time = 0;
let stats = { particles: 0, fps: 0 };

function init() {
    // Scene
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x000000, 0.0005);

    // Camera
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 2000);
    camera.position.z = 500;

    // Renderer
    const canvas = document.getElementById('canvas');
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Create particle systems for each color
    createParticleSystems();

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0xffffff, 1, 1000);
    pointLight.position.set(0, 0, 250);
    scene.add(pointLight);

    // Event listeners
    window.addEventListener('resize', onWindowResize);
    document.addEventListener('mousemove', onMouseMove);

    // Control buttons
    document.querySelectorAll('.control-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.control-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            mode = btn.dataset.mode;
        });
    });

    // Populate palette info
    updatePaletteDisplay();

    // Animation loop
    animate();
}

function createParticleSystems() {
    const particlesPerColor = 800;
    const spreadRadius = 300;

    PALETTE.forEach((color, colorIndex) => {
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(particlesPerColor * 3);
        const velocities = [];
        const originalPositions = [];

        for (let i = 0; i < particlesPerColor; i++) {
            // Create sphere distribution
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos(2 * Math.random() - 1);
            const radius = spreadRadius * (0.5 + Math.random() * 0.5);

            const x = radius * Math.sin(phi) * Math.cos(theta);
            const y = radius * Math.sin(phi) * Math.sin(theta);
            const z = radius * Math.cos(phi);

            positions[i * 3] = x;
            positions[i * 3 + 1] = y;
            positions[i * 3 + 2] = z;

            originalPositions.push(new THREE.Vector3(x, y, z));

            velocities.push({
                x: (Math.random() - 0.5) * 0.5,
                y: (Math.random() - 0.5) * 0.5,
                z: (Math.random() - 0.5) * 0.5
            });
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

        const material = new THREE.PointsMaterial({
            color: new THREE.Color(...color.rgb),
            size: 3,
            transparent: true,
            opacity: 0.8,
            blending: THREE.AdditiveBlending,
            depthWrite: false
        });

        const particleSystem = new THREE.Points(geometry, material);

        // Store metadata
        particleSystem.userData = {
            velocities,
            originalPositions,
            colorIndex,
            baseColor: color.rgb
        };

        scene.add(particleSystem);
        particles.push(particleSystem);
        stats.particles += particlesPerColor;
    });
}

function updateParticles() {
    particles.forEach((system, sysIndex) => {
        const positions = system.geometry.attributes.position.array;
        const { velocities, originalPositions, baseColor } = system.userData;

        for (let i = 0; i < positions.length / 3; i++) {
            const idx = i * 3;
            let x = positions[idx];
            let y = positions[idx + 1];
            let z = positions[idx + 2];

            switch (mode) {
                case 'orbit':
                    // Orbital motion around origin
                    const orbitSpeed = 0.0005;
                    const distance = Math.sqrt(x * x + y * y + z * z);
                    const angle = Math.atan2(y, x) + orbitSpeed;
                    x = distance * Math.cos(angle);
                    y = distance * Math.sin(angle);
                    z += Math.sin(time * 0.001 + i) * 0.1;
                    break;

                case 'attract':
                    // Attract to mouse position
                    const dx = mouseX - x;
                    const dy = mouseY - y;
                    const dz = mouseZ - z;
                    const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
                    const force = Math.min(1, 5000 / (dist + 1));

                    velocities[i].x += dx * force * 0.0001;
                    velocities[i].y += dy * force * 0.0001;
                    velocities[i].z += dz * force * 0.0001;

                    x += velocities[i].x;
                    y += velocities[i].y;
                    z += velocities[i].z;

                    // Damping
                    velocities[i].x *= 0.95;
                    velocities[i].y *= 0.95;
                    velocities[i].z *= 0.95;
                    break;

                case 'explode':
                    // Explode from mouse
                    const edx = x - mouseX;
                    const edy = y - mouseY;
                    const edz = z - mouseZ;
                    const eDist = Math.sqrt(edx * edx + edy * edy + edz * edz);
                    const eForce = Math.min(1, 10000 / (eDist + 1));

                    velocities[i].x += edx * eForce * 0.0002;
                    velocities[i].y += edy * eForce * 0.0002;
                    velocities[i].z += edz * eForce * 0.0002;

                    x += velocities[i].x;
                    y += velocities[i].y;
                    z += velocities[i].z;

                    velocities[i].x *= 0.98;
                    velocities[i].y *= 0.98;
                    velocities[i].z *= 0.98;
                    break;

                case 'harmony':
                    // Arrange in color harmony pattern
                    const harmonyAngle = (sysIndex / particles.length) * Math.PI * 2;
                    const harmonyRadius = 400;
                    const targetX = Math.cos(harmonyAngle + time * 0.001) * harmonyRadius;
                    const targetY = Math.sin(harmonyAngle + time * 0.001) * harmonyRadius;
                    const targetZ = Math.sin(time * 0.002 + i * 0.01) * 100;

                    x += (targetX - x) * 0.01;
                    y += (targetY - y) * 0.01;
                    z += (targetZ - z) * 0.01;
                    break;
            }

            positions[idx] = x;
            positions[idx + 1] = y;
            positions[idx + 2] = z;
        }

        system.geometry.attributes.position.needsUpdate = true;

        // Pulse effect
        system.material.opacity = 0.6 + Math.sin(time * 0.002 + sysIndex) * 0.2;
    });
}

function animate() {
    requestAnimationFrame(animate);

    time++;

    updateParticles();

    // Camera rotation
    camera.position.x = Math.sin(time * 0.0001) * 50;
    camera.lookAt(0, 0, 0);

    renderer.render(scene, camera);

    // Update stats
    if (time % 60 === 0) {
        updateStats();
    }
}

function onMouseMove(event) {
    // Convert mouse position to 3D coordinates
    mouseX = (event.clientX / window.innerWidth) * 2 - 1;
    mouseY = -(event.clientY / window.innerHeight) * 2 + 1;

    mouseX *= 500;
    mouseY *= 500;
    mouseZ = 0;

    // Update custom cursor
    const cursor = document.getElementById('cursor');
    cursor.style.left = event.clientX + 'px';
    cursor.style.top = event.clientY + 'px';

    if (mode === 'attract') {
        cursor.style.transform = 'scale(2)';
    } else if (mode === 'explode') {
        cursor.style.transform = 'scale(1.5)';
        cursor.style.borderColor = '#ff006e';
    } else {
        cursor.style.transform = 'scale(1)';
        cursor.style.borderColor = 'white';
    }
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function updatePaletteDisplay() {
    const container = document.getElementById('paletteList');
    container.innerHTML = PALETTE.map(color => `
        <div class="color-sample">
            <div class="color-dot" style="background-color: ${color.hex};"></div>
            <div class="color-label">${color.hex}</div>
        </div>
    `).join('');
}

function updateStats() {
    const statsEl = document.getElementById('stats');
    statsEl.innerHTML = `
        Particles: ${stats.particles.toLocaleString()}<br>
        Mode: ${mode.toUpperCase()}<br>
        Colors: ${PALETTE.length}
    `;
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
