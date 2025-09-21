import { Camera, Zap, Sparkles, ChefHat } from 'lucide-react';

export const HowItWorks = () => {
  const steps = [
    {
      icon: Camera,
      number: '01',
      title: "Capture The Moment",
      description: "Snap or upload any meal photo. Our AI recognizes over 10,000 foods and dishes from around the world.",
      color: "primary",
      bgGradient: "from-primary/20 to-primary/5"
    },
    {
      icon: ChefHat,
      number: '02', 
      title: "AI Chef Analysis",
      description: "Advanced computer vision identifies ingredients, cooking methods, and portion sizes with restaurant-grade precision.",
      color: "secondary",
      bgGradient: "from-secondary/20 to-secondary/5"
    },
    {
      icon: Sparkles,
      number: '03',
      title: "Instant Insights",
      description: "Get detailed nutrition facts, health scores, and personalized recommendations in under 3 seconds.",
      color: "accent", 
      bgGradient: "from-accent/20 to-accent/5"
    }
  ];

  return (
    <section className="py-20 lg:py-32 relative">
      {/* Background Elements */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-muted/20 to-transparent"></div>
      
      <div className="container mx-auto px-4 relative">
        <div className="text-center mb-20">
          <div className="inline-flex items-center gap-2 bg-accent/10 text-accent px-4 py-2 rounded-full text-sm font-medium mb-6">
            <Zap className="w-4 h-4" />
            Simple. Smart. Lightning Fast.
          </div>
          <h2 className="text-4xl md:text-5xl lg:text-6xl font-bold text-foreground mb-6">
            How The Magic 
            <span className="gradient-text block">Happens</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            Three simple steps to transform any meal photo into actionable nutrition intelligence
          </p>
        </div>
        
        <div className="grid lg:grid-cols-3 gap-12 max-w-6xl mx-auto">
          {steps.map((step, index) => {
            const Icon = step.icon;
            const colorClass = `text-${step.color}`;
            
            return (
              <div 
                key={index} 
                className="group relative animate-slide-up" 
                style={{animationDelay: `${index * 0.2}s`}}
              >
                {/* Connection Line (Desktop) */}
                {index < steps.length - 1 && (
                  <div className="hidden lg:block absolute top-16 left-full w-12 h-px bg-gradient-to-r from-border to-transparent z-0"></div>
                )}
                
                <div className="interactive-card text-center relative z-10 h-full group">
                  {/* Step Number */}
                  <div className="absolute -top-4 -left-4 w-12 h-12 bg-gradient-warmth rounded-full flex items-center justify-center shadow-primary">
                    <span className="text-primary-foreground font-bold text-lg">{step.number}</span>
                  </div>
                  
                  {/* Icon */}
                  <div className={`w-20 h-20 mx-auto mb-6 bg-gradient-to-br ${step.bgGradient} rounded-2xl flex items-center justify-center shadow-soft group-hover:scale-110 transition-transform duration-300`}>
                    <Icon className={`w-10 h-10 ${colorClass}`} />
                  </div>
                  
                  {/* Content */}
                  <h3 className="text-2xl font-bold text-card-foreground mb-4 group-hover:gradient-text transition-all duration-300">
                    {step.title}
                  </h3>
                  <p className="text-muted-foreground leading-relaxed text-lg">
                    {step.description}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};