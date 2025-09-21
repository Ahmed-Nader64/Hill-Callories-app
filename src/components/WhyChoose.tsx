import { Brain, Timer, Smartphone, Target, Shield, Users } from 'lucide-react';

export const WhyChoose = () => {
  const features = [
    {
      icon: Brain,
      title: "Restaurant-Grade Accuracy",
      description: "Trained on millions of real meals from professional kitchens worldwide. Our AI understands food like a nutritionist.",
      color: "primary",
      stats: "99.2% accuracy"
    },
    {
      icon: Timer,
      title: "Lightning Fast Results",
      description: "From photo to complete nutrition breakdown in under 3 seconds. No tedious manual logging ever again.",
      color: "secondary", 
      stats: "<3 seconds"
    },
    {
      icon: Target,
      title: "Personalized Insights",
      description: "Get health recommendations tailored to your dietary goals, restrictions, and lifestyle preferences.",
      color: "accent",
      stats: "AI-powered"
    }
  ];

  return (
    <section className="py-20 lg:py-32 bg-gradient-to-br from-muted/40 via-muted/20 to-muted/40 relative">
      {/* Decorative Elements */}
      <div className="absolute top-10 left-1/4 w-32 h-32 bg-primary/10 rounded-full blur-2xl"></div>
      <div className="absolute bottom-10 right-1/4 w-40 h-40 bg-secondary/10 rounded-full blur-3xl"></div>
      
      <div className="container mx-auto px-4 relative">
        <div className="text-center mb-20">
          <div className="inline-flex items-center gap-2 bg-secondary/10 text-secondary px-4 py-2 rounded-full text-sm font-medium mb-6">
            <Shield className="w-4 h-4" />
            Trusted By Food Lovers Worldwide
          </div>
          <h2 className="text-4xl md:text-5xl lg:text-6xl font-bold text-foreground mb-6">
            Why Food Experts Choose
            <span className="gradient-text block">Hill Calories AI</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            We don't just count calories—we understand the story behind every meal
          </p>
        </div>
        
        <div className="grid lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            const colorClass = feature.color === 'primary' ? 'text-primary' : 
                               feature.color === 'secondary' ? 'text-secondary' : 
                               'text-accent';
            const bgClass = feature.color === 'primary' ? 'from-primary/20 to-primary/5' : 
                           feature.color === 'secondary' ? 'from-secondary/20 to-secondary/5' : 
                           'from-accent/20 to-accent/5';
            
            return (
              <div 
                key={index} 
                className="group animate-slide-up"
                style={{animationDelay: `${index * 0.15}s`}}
              >
                <div className="interactive-card h-full relative overflow-hidden group">
                  {/* Gradient Overlay */}
                  <div className={`absolute inset-0 bg-gradient-to-br ${bgClass} opacity-0 group-hover:opacity-100 transition-opacity duration-300`}></div>
                  
                  <div className="relative z-10">
                    {/* Stats Badge */}
                    <div className="absolute top-4 right-4 bg-card border border-border/50 px-3 py-1 rounded-full">
                      <span className={`text-sm font-bold ${colorClass}`}>{feature.stats}</span>
                    </div>
                    
                    {/* Icon */}
                    <div className={`w-16 h-16 mb-8 bg-gradient-to-br ${bgClass} rounded-2xl flex items-center justify-center shadow-soft group-hover:scale-110 group-hover:rotate-3 transition-all duration-300`}>
                      <Icon className={`w-8 h-8 ${colorClass}`} />
                    </div>
                    
                    {/* Content */}
                    <h3 className="text-2xl font-bold text-card-foreground mb-6 group-hover:gradient-text transition-all duration-300">
                      {feature.title}
                    </h3>
                    <p className="text-muted-foreground leading-relaxed text-lg">
                      {feature.description}
                    </p>
                    
                    {/* Hover Arrow */}
                    <div className={`mt-6 flex items-center gap-2 ${colorClass} opacity-0 group-hover:opacity-100 transform translate-x-2 group-hover:translate-x-0 transition-all duration-300`}>
                      <span className="text-sm font-medium">Learn more</span>
                      <div className="w-4 h-4 border-r-2 border-b-2 border-current rotate-[-45deg] group-hover:translate-x-1 transition-transform duration-200"></div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
        
        {/* Bottom Trust Elements */}
        <div className="mt-20 flex justify-center items-center gap-12 opacity-60">
          <div className="flex items-center gap-3">
            <Users className="w-6 h-6 text-muted-foreground" />
            <span className="text-muted-foreground font-medium">500K+ Active Users</span>
          </div>
          <div className="w-px h-6 bg-border"></div>
          <div className="flex items-center gap-3">
            <Shield className="w-6 h-6 text-muted-foreground" />
            <span className="text-muted-foreground font-medium">HIPAA Compliant</span>
          </div>
          <div className="w-px h-6 bg-border"></div>
          <div className="flex items-center gap-3">
            <Brain className="w-6 h-6 text-muted-foreground" />
            <span className="text-muted-foreground font-medium">FDA Recognized</span>
          </div>
        </div>
      </div>
    </section>
  );
};