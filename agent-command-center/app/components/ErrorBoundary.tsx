'use client';

import { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
    children?: ReactNode;
}

interface State {
    hasError: boolean;
    error: Error | null;
}

export default class ErrorBoundary extends Component<Props, State> {
    public state: State = {
        hasError: false,
        error: null,
    };

    public static getDerivedStateFromError(error: Error): State {
        return { hasError: true, error };
    }

    public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
        console.error('Uncaught error:', error, errorInfo);
    }

    public render() {
        if (this.state.hasError) {
            return (
                <div className="min-h-screen bg-black text-white p-10 font-mono">
                    <h1 className="text-2xl text-red-500 mb-4">CRITICAL SYSTEM FAILURE</h1>
                    <p className="mb-4">The visual interface failed to interpret the data stream.</p>
                    <pre className="bg-gray-900 p-4 rounded border border-red-900 overflow-auto text-xs">
                        {this.state.error?.message}
                        {'\n'}
                        {this.state.error?.stack}
                    </pre>
                    <button
                        onClick={() => window.location.reload()}
                        className="mt-6 px-4 py-2 bg-red-900 hover:bg-red-700 text-white rounded"
                    >
                        ATTEMPT SYSTEM REBOOT
                    </button>
                </div>
            );
        }

        return this.props.children;
    }
}
