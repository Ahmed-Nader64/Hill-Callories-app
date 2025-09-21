import { Button } from '@/components/ui/button';
import { Camera, ArrowRight, Sparkles, Shield, Users, Zap } from 'lucide-react';

interface ClosingCTAProps {
  onGetStarted: () => void;
}

export const ClosingCTA = ({ onGetStarted }: ClosingCTAProps) => {
  return (
    <section className="py-24 lg:py-32 relative overflow-hidden">
      {/* Dynamic Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-secondary/5 to-accent/10"></div>
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-gradient-warmth rounded-full blur-3xl opacity-30 animate-float"></div>
      <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-gradient-depth rounded-full blur-3xl opacity-20 animate-float" style={{animationDelay: '2s'}}></div>
      
      <div className="container mx-auto px-4 relative">
        <div className="max-w-5xl mx-auto text-center">
          <div className="space-y-12">
            {/* Badge & Headline */}
            <div className="space-y-8 animate-slide-up">
              <div className="inline-flex items-center gap-2 bg-primary/10 text-primary px-6 py-3 rounded-full text-base font-medium">
                <Sparkles className="w-5 h-5" />
                Ready To Transform Your Nutrition Journey?
              </div>
              
              <h2 className="text-4xl md:text-6xl lg:text-7xl font-bold text-foreground leading-tight">
                Stop Guessing.
                <br />
                <span className="gradient-text">Start Knowing.</span>
              </h2>
              
              <p className="text-2xl lg:text-3xl text-muted-foreground max-w-3xl mx-auto font-light leading-relaxed">
                Join the food revolution that's helping people make smarter choices, one meal at a time.
              </p>
            </div>
            
            {/* Main CTA */}
            <div className="animate-slide-up" style={{animationDelay: '0.3s'}}>
              <Button
                onClick={onGetStarted}
                className="food-button text-2xl px-12 py-8 h-auto group shadow-depth animate-pulse-glow"
              >
                <Camera className="w-8 h-8 mr-4 group-hover:rotate-12 transition-transform duration-300" />
                Start Your Food Journey
                <ArrowRight className="w-6 h-6 ml-4 group-hover:translate-x-2 transition-transform duration-300" />
              </Button>
              
              <p className="mt-6 text-lg text-muted-foreground">
                🚀 <strong>Free forever plan</strong> • 📱 Works on any device • ⚡ Results in 3 seconds
              </p>
            </div>
            
            {/* Trust Elements */}
            <div className="grid md:grid-cols-3 gap-8 mt-16 animate-slide-up" style={{animationDelay: '0.6s'}}>
              <div className="flex flex-col items-center space-y-4 p-6 bg-card/50 backdrop-blur-sm rounded-2xl border border-border/30 hover-lift">
                <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center">
                  <Shield className="w-8 h-8 text-primary" />
                </div>
                <div className="text-center">
                  <div className="font-bold text-lg text-foreground">Privacy First</div>
                  <div className="text-sm text-muted-foreground">Your food photos stay on your device</div>
                </div>
              </div>
              
              <div className="flex flex-col items-center space-y-4 p-6 bg-card/50 backdrop-blur-sm rounded-2xl border border-border/30 hover-lift">
                <div className="w-16 h-16 bg-secondary/10 rounded-full flex items-center justify-center">
                  <Users className="w-8 h-8 text-secondary" />
                </div>
                <div className="text-center">
                  <div className="font-bold text-lg text-foreground">500K+ Users</div>
                  <div className="text-sm text-muted-foreground">Trusted by food professionals worldwide</div>
                </div>
              </div>
              
              <div className="flex flex-col items-center space-y-4 p-6 bg-card/50 backdrop-blur-sm rounded-2xl border border-border/30 hover-lift">
                <div className="w-16 h-16 bg-accent/10 rounded-full flex items-center justify-center">
                  <Zap className="w-8 h-8 text-accent" />
                </div>
                <div className="text-center">
                  <div className="font-bold text-lg text-foreground">Lightning Fast</div>
                  <div className="text-sm text-muted-foreground">Complete analysis in under 3 seconds</div>
                </div>
              </div>
            </div>
            
            {/* Final Push */}
            <div className="mt-16 p-8 bg-gradient-to-r from-card/80 to-card/60 backdrop-blur-sm rounded-2xl border border-border/30 animate-slide-up" style={{animationDelay: '0.9s'}}>
              <div className="text-center space-y-4">
                <div className="text-lg font-medium text-foreground">
                  🎯 Perfect for nutritionists, chefs, fitness enthusiasts, and curious food lovers
                </div>
                <div className="text-sm text-muted-foreground">
                  No credit card • No signup required • Start analyzing in 30 seconds
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};