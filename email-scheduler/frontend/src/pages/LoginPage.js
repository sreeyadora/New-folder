import React from 'react';
import { Mail } from 'lucide-react';

export default function LoginPage() {
  const handleGoogleLogin = () => {
    const redirectUrl = window.location.origin + '/dashboard';
    window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(
      redirectUrl
    )}`;
  };

  return (
    <div className="min-h-screen flex">
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-primary/10 via-accent to-background items-center justify-center p-12">
        <div className="max-w-md">
          <div className="flex items-center space-x-3 mb-6">
            <div className="p-3 bg-primary rounded-2xl">
              <Mail className="h-8 w-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold text-foreground">
              ReachInbox
            </h1>
          </div>
          <p className="text-lg text-muted-foreground leading-relaxed">
            Production-grade email scheduler. Schedule, send, and track emails at scale.
          </p>
        </div>
      </div>

      <div className="flex-1 flex items-center justify-center p-8 bg-background">
        <div className="w-full max-w-md space-y-8">
          <div className="text-center">
            <h2 className="text-3xl font-semibold text-foreground mb-2">
              Welcome Back
            </h2>
            <p className="text-muted-foreground">
              Sign in to continue
            </p>
          </div>

          <div className="bg-card border border-border rounded-xl shadow-sm p-8">
            <button
              onClick={handleGoogleLogin}
              className="w-full flex items-center justify-center space-x-3 px-6 py-3 border-2 border-input bg-white hover:bg-accent transition-all rounded-full font-medium"
            >
              <Mail className="h-5 w-5" />
              <span>Continue with Google</span>
            </button>

            <div className="mt-6 text-center text-sm text-muted-foreground">
              By signing in, you agree to our policies
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
