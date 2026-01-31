'use client';

export default function NeuralCables() {
    return (
        <div className="absolute inset-0 pointer-events-none z-0 overflow-visible" style={{ transform: 'translateZ(-10px)' }}>
            <svg width="100%" height="100%" className="overflow-visible opacity-60">
                <defs>
                    <linearGradient id="cable-gradient-left" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor="rgba(0, 255, 249, 0.1)" />
                        <stop offset="50%" stopColor="rgba(0, 255, 249, 0.8)" />
                        <stop offset="100%" stopColor="rgba(0, 255, 249, 0.1)" />
                    </linearGradient>
                    <linearGradient id="cable-gradient-right" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor="rgba(255, 174, 0, 0.1)" />
                        <stop offset="50%" stopColor="rgba(255, 174, 0, 0.8)" />
                        <stop offset="100%" stopColor="rgba(255, 174, 0, 0.1)" />
                    </linearGradient>
                    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                        <feGaussianBlur stdDeviation="4" result="blur" />
                        <feComposite in="SourceGraphic" in2="blur" operator="over" />
                    </filter>
                </defs>

                {/* Left Side Cables (Agents -> Profile) */}
                {/* Top Connection */}
                <path
                    d="M 350 250 C 450 250, 550 350, 700 350"
                    stroke="url(#cable-gradient-left)"
                    strokeWidth="3"
                    fill="none"
                    filter="url(#glow)"
                    className="animate-pulse"
                />
                {/* Bottom Connection */}
                <path
                    d="M 350 450 C 450 450, 550 400, 700 400"
                    stroke="url(#cable-gradient-left)"
                    strokeWidth="2"
                    fill="none"
                    opacity="0.5"
                />

                {/* Right Side Cables (Missions -> Profile) */}
                {/* Top Connection */}
                <path
                    d="M 1550 250 C 1450 250, 1350 350, 1200 350"
                    stroke="url(#cable-gradient-right)"
                    strokeWidth="3"
                    fill="none"
                    filter="url(#glow)"
                    className="animate-pulse"
                />
                {/* Bottom Connection */}
                <path
                    d="M 1550 450 C 1450 450, 1350 400, 1200 400"
                    stroke="url(#cable-gradient-right)"
                    strokeWidth="2"
                    fill="none"
                    opacity="0.5"
                />
            </svg>
        </div>
    );
}
