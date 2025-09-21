import { useRef } from 'react';
import { Header } from '@/components/Header';
import { Hero } from '@/components/Hero';
import { SocialProof } from '@/components/SocialProof';
import { HowItWorks } from '@/components/HowItWorks';
import { NutritionAnalyzer } from '@/components/NutritionAnalyzer';
import { WhyChoose } from '@/components/WhyChoose';
import { Testimonials } from '@/components/Testimonials';
import { ClosingCTA } from '@/components/ClosingCTA';

const Index = () => {
  const analyzerRef = useRef<HTMLElement>(null);

  const scrollToAnalyzer = () => {
    analyzerRef.current?.scrollIntoView({ 
      behavior: 'smooth',
      block: 'center'
    });
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <Header />
      
      {/* Hero Section */}
      <Hero onGetStarted={scrollToAnalyzer} />
      
      {/* Social Proof */}
      <SocialProof />
      
      {/* How It Works */}
      <HowItWorks />
      
      {/* Interactive Nutrition Analyzer */}
      <section 
        ref={analyzerRef}
        className="py-16 lg:py-24 bg-muted/10"
      >
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              Try It Now - Upload Your Meal
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Experience the power of AI nutrition analysis with your own meal photos
            </p>
          </div>
          <NutritionAnalyzer />
        </div>
      </section>

      {/* Why Choose */}
      <WhyChoose />
      
      {/* Testimonials */}
      <Testimonials />
      
      {/* Closing CTA */}
      <ClosingCTA onGetStarted={scrollToAnalyzer} />

      {/* Footer */}
      <footer className="py-12 px-4 border-t border-border bg-muted/30">
        <div className="container mx-auto text-center">
          <div className="mb-8">
            <h3 className="text-xl font-bold text-foreground mb-2">Hill Calories AI</h3>
            <p className="text-muted-foreground">
              Revolutionizing nutrition tracking with artificial intelligence
            </p>
          </div>
          <div className="flex justify-center gap-8 text-sm text-muted-foreground mb-6">
            <a href="#privacy" className="hover:text-primary transition-smooth">Privacy</a>
            <a href="#terms" className="hover:text-primary transition-smooth">Terms</a>
            <a href="#contact" className="hover:text-primary transition-smooth">Contact</a>
            <a href="#api" className="hover:text-primary transition-smooth">API</a>
          </div>
          <div className="pt-6 border-t border-border">
            <p className="text-xs text-muted-foreground">
              © 2024 Hill Calories AI. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;