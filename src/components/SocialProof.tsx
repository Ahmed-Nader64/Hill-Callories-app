import { Star, Users, Award, TrendingUp } from 'lucide-react';

export const SocialProof = () => {
  return (
    <section className="py-12 bg-gradient-to-r from-muted/30 via-muted/20 to-muted/30 border-y border-border/50">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 items-center">
          {/* App Store Rating */}
          <div className="flex flex-col items-center text-center space-y-2 hover-lift">
            <div className="flex items-center gap-2 mb-1">
              <div className="flex">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="w-4 h-4 text-accent fill-accent" />
                ))}
              </div>
              <span className="font-bold text-foreground">4.9</span>
            </div>
            <div className="text-sm text-muted-foreground">App Store Rating</div>
            <div className="text-xs text-muted-foreground">2,847 reviews</div>
          </div>
          
          {/* Users Count */}
          <div className="flex flex-col items-center text-center space-y-2 hover-lift">
            <Users className="w-8 h-8 text-primary mb-1" />
            <div className="font-bold text-2xl text-foreground">500K+</div>
            <div className="text-sm text-muted-foreground">Active Food Lovers</div>
          </div>
          
          {/* Awards */}
          <div className="flex flex-col items-center text-center space-y-2 hover-lift">
            <Award className="w-8 h-8 text-secondary mb-1" />
            <div className="font-bold text-foreground">#1 Nutrition</div>
            <div className="text-sm text-muted-foreground">Health & Fitness</div>
          </div>
          
          {/* Accuracy */}
          <div className="flex flex-col items-center text-center space-y-2 hover-lift">
            <TrendingUp className="w-8 h-8 text-accent mb-1" />
            <div className="font-bold text-2xl text-foreground">99.2%</div>
            <div className="text-sm text-muted-foreground">Analysis Accuracy</div>
          </div>
        </div>
        
        {/* Press Mentions */}
        <div className="mt-8 pt-8 border-t border-border/50">
          <div className="text-center text-sm text-muted-foreground mb-4">
            Featured In
          </div>
          <div className="flex flex-wrap justify-center items-center gap-8">
            {['TechCrunch', 'Product Hunt', 'App Store Today', 'Nutrition Today'].map((publication) => (
              <div key={publication} className="px-4 py-2 bg-card rounded-lg border border-border/30 hover:border-primary/30 transition-colors duration-200">
                <span className="font-medium text-foreground/80">{publication}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};