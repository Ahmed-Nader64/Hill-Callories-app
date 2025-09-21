import { Button } from '@/components/ui/button';
import { Camera, Sparkles, ArrowRight } from 'lucide-react';

interface HeroProps {
  onGetStarted: () => void;
}

export const Hero = ({ onGetStarted }: HeroProps) => {
  return (
    <section className="py-20 lg:py-32 relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-secondary/5"></div>
      <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-gradient-warmth rounded-full blur-3xl opacity-20 animate-float"></div>
      
      <div className="container mx-auto px-4 relative">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          {/* Left Side - Compelling Copy */}
          <div className="space-y-10 animate-slide-up">
            <div className="space-y-8">
              <div className="inline-flex items-center gap-2 bg-primary/10 text-primary px-4 py-2 rounded-full text-sm font-medium">
                <Sparkles className="w-4 h-4" />
                Stop Guessing What's In Your Food
              </div>
              
              <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold leading-tight">
                Every Meal Tells
                <br />
                <span className="gradient-text">
                  A Story
                </span>
              </h1>
              
              <p className="text-xl lg:text-2xl text-muted-foreground leading-relaxed font-light">
                Discover the hidden nutrition in every bite with AI that understands food like a chef, analyzes like a scientist.
              </p>
            </div>

            {/* Single Strong CTA */}
            <div className="flex flex-col space-y-4">
              <Button
                onClick={onGetStarted}
                className="food-button text-xl px-10 py-8 h-auto group animate-pulse-glow"
              >
                <Camera className="w-6 h-6 mr-4 group-hover:rotate-12 transition-transform duration-300" />
                Reveal My Meal's Secrets
                <ArrowRight className="w-5 h-5 ml-4 group-hover:translate-x-1 transition-transform duration-300" />
              </Button>
              
              <p className="text-sm text-muted-foreground text-center">
                ✨ No signup required • 🔬 Instant analysis • 🎯 Precise nutrition data
              </p>
            </div>
          </div>

          {/* Right Side - Interactive Food Demo */}
          <div className="relative animate-slide-up" style={{animationDelay: '0.3s'}}>
            <div className="interactive-card bg-gradient-card shadow-depth p-8 relative overflow-hidden">
              {/* Animated Background Elements */}
              <div className="absolute top-4 right-4 w-20 h-20 bg-accent/10 rounded-full animate-pulse"></div>
              <div className="absolute bottom-4 left-4 w-16 h-16 bg-secondary/10 rounded-full animate-float"></div>
              
              {/* Food Photo Upload Demo */}
              <div className="bg-gradient-to-br from-muted/30 to-muted/10 rounded-2xl p-8 mb-8 border-2 border-dashed border-primary/20 hover:border-primary/40 transition-colors duration-300">
                <div className="aspect-square bg-gradient-warmth/20 rounded-xl flex items-center justify-center mb-6 hover-lift">
                  <div className="text-center">
                    <Camera className="w-20 h-20 text-primary mx-auto mb-4 animate-pulse" />
                    <div className="text-primary font-semibold">Perfect pasta detected!</div>
                  </div>
                </div>
                
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Analyzing ingredients...</span>
                    <div className="w-24 bg-primary/20 rounded-full h-2">
                      <div className="bg-gradient-warmth h-2 rounded-full w-full animate-pulse"></div>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Rich Nutrition Results */}
              <div className="space-y-4">
                <div className="flex justify-between items-center p-4 bg-gradient-warmth/10 rounded-xl border border-primary/20 hover-lift">
                  <span className="font-semibold text-card-foreground">Total Calories</span>
                  <span className="text-2xl font-bold gradient-text">524</span>
                </div>
                
                <div className="grid grid-cols-3 gap-3">
                  <div className="text-center p-4 bg-gradient-to-br from-secondary/10 to-secondary/5 rounded-xl hover-lift">
                    <div className="text-xl font-bold text-secondary">28g</div>
                    <div className="text-xs text-muted-foreground font-medium">Protein</div>
                  </div>
                  <div className="text-center p-4 bg-gradient-to-br from-accent/10 to-accent/5 rounded-xl hover-lift">
                    <div className="text-xl font-bold text-accent">65g</div>
                    <div className="text-xs text-muted-foreground font-medium">Carbs</div>
                  </div>
                  <div className="text-center p-4 bg-gradient-to-br from-primary/10 to-primary/5 rounded-xl hover-lift">
                    <div className="text-xl font-bold text-primary">18g</div>
                    <div className="text-xs text-muted-foreground font-medium">Healthy Fats</div>
                  </div>
                </div>
                
                <div className="mt-6 p-4 bg-gradient-depth/5 rounded-xl border border-secondary/20">
                  <div className="text-xs text-muted-foreground mb-2">Key Ingredients Detected</div>
                  <div className="flex flex-wrap gap-2">
                    {['Basil', 'Parmesan', 'Pine Nuts', 'Olive Oil'].map((ingredient, i) => (
                      <span key={i} className="bg-accent/20 text-accent px-3 py-1 rounded-full text-xs font-medium">
                        {ingredient}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};