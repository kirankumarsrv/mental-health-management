import React from 'react';

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }

    componentDidCatch(error, errorInfo) {
        console.error('UI crashed:', error, errorInfo);
    }

    handleReload = () => {
        window.location.reload();
    };

    render() {
        if (this.state.hasError) {
            return (
                <div style={{ padding: '2rem' }}>
                    <h2>Something went wrong.</h2>
                    <p style={{ color: 'var(--text-muted)' }}>
                        {this.state.error?.message || 'Unknown error'}
                    </p>
                    <button className="btn" onClick={this.handleReload}>
                        Reload
                    </button>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;
