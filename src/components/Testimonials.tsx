import { Star, Quote, Heart, Zap, Target } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

export const Testimonials = () => {
  const testimonials = [
    {
      name: "Sarah Chen",
      role: "Registered Dietitian", 
      location: "San Francisco, CA",
      content: "Finally, an app that gets nutrition right. My clients love how it recognizes complex dishes my grandmother makes. The accuracy rivals professional food analysis software.",
      rating: 5,
      avatar: "SC",
      highlight: "Professional-grade accuracy",
      verified: true
    },
    {
      name: "Marcus Rodriguez",
      role: "Fitness Coach",
      location: "Miami, FL", 
      content: "Game-changer for meal prep tracking. Takes 2 seconds to analyze my entire weekly meal prep. My athletes are hitting their macro targets consistently now.",
      rating: 5,
      avatar: "MR",
      highlight: "Perfect for meal prep",
      verified: true
    },
    {
      name: "Elena Nakamura",
      role: "Busy Parent & Chef",
      location: "Portland, OR",
      content: "As a working mom who loves cooking, this saves me hours of nutrition research. It even recognizes my fusion recipes and dietary modifications perfectly.",
      rating: 5,
      avatar: "EN", 
      highlight: "Recognizes complex recipes",
      verified: true
    }
  ];

  return (
    <section className="py-20 lg:py-32 bg-gradient-to-br from-card via-background to-card relative">
      {/* Decorative Elements */}
      <div className="absolute top-20 right-20 w-24 h-24 bg-accent/20 rounded-full blur-2xl animate-float"></div>
      <div className="absolute bottom-20 left-20 w-32 h-32 bg-primary/20 rounded-full blur-3xl animate-float" style={{animationDelay: '1s'}}></div>
      
      <div className="container mx-auto px-4 relative">
        <div className="text-center mb-20">
          <div className="inline-flex items-center gap-2 bg-accent/10 text-accent px-4 py-2 rounded-full text-sm font-medium mb-6">
            <Heart className="w-4 h-4" />
            Loved By Food Professionals
          </div>
          <h2 className="text-4xl md:text-5xl lg:text-6xl font-bold text-foreground mb-6">
            Real Stories From
            <span className="gradient-text block">Real Food Lovers</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            Join thousands of nutrition professionals, chefs, and food enthusiasts who've revolutionized their approach to food analysis
          </p>
        </div>
        
        <div className="grid lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
          {testimonials.map((testimonial, index) => (
            <Card 
              key={index} 
              className="interactive-card border-0 shadow-depth hover:shadow-depth bg-gradient-card relative overflow-hidden group animate-slide-up"
              style={{animationDelay: `${index * 0.2}s`}}
            >
              <CardContent className="p-8 relative z-10">
                {/* Verified Badge */}
                {testimonial.verified && (
                  <div className="absolute top-6 right-6 bg-primary/10 text-primary px-3 py-1 rounded-full text-xs font-medium flex items-center gap-1">
                    <div className="w-2 h-2 bg-primary rounded-full"></div>
                    Verified
                  </div>
                )}
                
                {/* Quote & Rating */}
                <div className="mb-8">
                  <div className="flex items-center justify-between mb-4">
                    <Quote className="w-10 h-10 text-primary/30" />
                    <div className="flex">
                      {[...Array(testimonial.rating)].map((_, i) => (
                        <Star key={i} className="w-4 h-4 text-accent fill-accent" />
                      ))}
                    </div>
                  </div>
                  <p className="text-card-foreground leading-relaxed text-lg mb-4 italic font-light">
                    "{testimonial.content}"
                  </p>
                  
                  {/* Highlight */}
                  <div className="inline-flex items-center gap-2 bg-secondary/10 text-secondary px-3 py-1 rounded-full text-sm font-medium">
                    <Target className="w-3 h-3" />
                    {testimonial.highlight}
                  </div>
                </div>
                
                {/* Author Info */}
                <div className="flex items-center gap-4">
                  <div className="relative">
                    <div className="w-14 h-14 bg-gradient-warmth rounded-full flex items-center justify-center shadow-soft">
                      <span className="text-primary-foreground font-bold text-lg">
                        {testimonial.avatar}
                      </span>
                    </div>
                    <div className="absolute -bottom-1 -right-1 w-5 h-5 bg-primary rounded-full flex items-center justify-center">
                      <div className="w-2 h-2 bg-primary-foreground rounded-full"></div>
                    </div>
                  </div>
                  <div className="flex-1">
                    <div className="font-bold text-card-foreground text-lg">
                      {testimonial.name}
                    </div>
                    <div className="text-sm text-primary font-medium">
                      {testimonial.role}
                    </div>
                    <div className="text-xs text-muted-foreground">
                      {testimonial.location}
                    </div>
                  </div>
                  <Zap className="w-5 h-5 text-accent opacity-60 group-hover:opacity-100 transition-opacity duration-300" />
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
        
        {/* Bottom CTA */}
        <div className="text-center mt-16">
          <p className="text-muted-foreground mb-4">
            Join 500K+ users who trust Hill Calories AI
          </p>
          <div className="flex justify-center items-center gap-6 text-sm">
            <div className="flex items-center gap-2 text-primary">
              <div className="w-2 h-2 bg-primary rounded-full"></div>
              <span>Used by nutritionists</span>
            </div>
            <div className="flex items-center gap-2 text-secondary">
              <div className="w-2 h-2 bg-secondary rounded-full"></div>
              <span>Trusted by chefs</span>
            </div>
            <div className="flex items-center gap-2 text-accent">
              <div className="w-2 h-2 bg-accent rounded-full"></div>
              <span>Loved by families</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};