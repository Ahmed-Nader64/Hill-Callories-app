import { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Camera, Upload, Loader2, Zap } from 'lucide-react';
import { toast } from '@/hooks/use-toast';

interface FoodItem {
  name: string;
  confidence: number;
  portion: {
    unit: string;
    value: number;
  };
  nutrition: {
    calories: number;
    protein: number;
    carbs: number;
    fat: number;
    fiber: number;
    sugar: number;
    sodium: number;
    cholesterol: number;
  };
}

interface NutritionData {
  status: string;
  timestamp: string;
  foods: FoodItem[];
  totals: {
    calories: number;
    protein: number;
    carbs: number;
    fat: number;
    fiber: number;
    sugar: number;
    sodium: number;
    cholesterol: number;
  };
  notes: string;
}

export const NutritionAnalyzer = () => {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [nutritionData, setNutritionData] = useState<NutritionData | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setSelectedImage(e.target?.result as string);
        setNutritionData(null);
      };
      reader.readAsDataURL(file);
    }
  };

  const analyzeNutrition = async () => {
    if (!selectedFile) return;
    
    setIsAnalyzing(true);
    
    try {
      const formData = new FormData();
      formData.append('image', selectedFile);

      const response = await fetch('https://4e87981ff717.ngrok-free.app/webhook/meal-ai', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to analyze meal');
      }

      const json = await response.json();
      const output = Array.isArray(json) ? json[0]?.output : json?.output;
      
      if (output && (output.food || output.foods || output.total || output.totals)) {
        // Handle new format with "food" and "total"
        const foods = output.food ? output.food.map((item: any) => ({
          name: item.name,
          confidence: item.confidence ?? 0.9,
          portion: {
            unit: 'serving',
            value: 1
          },
          nutrition: {
            calories: item.calories ?? 0,
            protein: item.protein ?? 0,
            carbs: item.carbs ?? 0,
            fat: item.fat ?? 0,
            fiber: item.fiber ?? 0,
            sugar: item.sugar ?? 0,
            sodium: item.sodium ?? 0,
            cholesterol: item.cholesterol ?? 0
          }
        })) : output.foods ?? [];
        
        const totals = output.total ? {
          calories: output.total.calories ?? 0,
          protein: output.total.protein ?? 0,
          carbs: output.total.carbs ?? 0,
          fat: output.total.fat ?? 0,
          fiber: output.total.fiber ?? 0,
          sugar: output.total.sugar ?? 0,
          sodium: output.total.sodium ?? 0,
          cholesterol: output.total.cholesterol ?? 0
        } : output.totals ?? { calories: 0, protein: 0, carbs: 0, fat: 0, fiber: 0, sugar: 0, sodium: 0, cholesterol: 0 };

        const normalized: NutritionData = {
          status: output.status,
          timestamp: output.timestamp ?? new Date().toISOString(),
          foods: foods,
          totals: totals,
          notes: output.notes ?? ''
        };
        setNutritionData(normalized);
        toast({
          title: "Analysis Complete!",
          description: "Your meal nutrition has been calculated.",
        });
      } else {
        console.error('Unexpected API response shape', json);
        throw new Error('Invalid response format');
      }
    } catch (error) {
      toast({
        title: "Analysis Failed",
        description: "Please try again with a clearer image.",
        variant: "destructive",
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current?.click();
  };

  const resetAnalysis = () => {
    setSelectedImage(null);
    setNutritionData(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      {/* Interactive Upload Section */}
      <Card className="bg-gradient-card shadow-xl border-0 overflow-hidden">
        <CardContent className="p-0">
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleImageUpload}
            className="hidden"
            capture="environment"
          />
          
          {!selectedImage ? (
            <div 
              className="relative p-12 cursor-pointer group hover:bg-muted/30 transition-all duration-300"
              onClick={triggerFileInput}
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => {
                e.preventDefault();
                const file = e.dataTransfer.files[0];
                if (file && file.type.startsWith('image/')) {
                  setSelectedFile(file);
                  const reader = new FileReader();
                  reader.onload = (event) => {
                    setSelectedImage(event.target?.result as string);
                    setNutritionData(null);
                  };
                  reader.readAsDataURL(file);
                }
              }}
            >
              <div className="text-center space-y-8">
                <div className="w-24 h-24 mx-auto bg-gradient-to-br from-primary/20 to-secondary/20 rounded-full flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                  <Camera className="w-12 h-12 text-primary" />
                </div>
                <div className="space-y-4">
                  <h3 className="text-2xl font-bold text-card-foreground">
                    Snap Your Meal
                  </h3>
                  <p className="text-lg text-muted-foreground max-w-md mx-auto">
                    Drag and drop an image here, or click to take a photo and get instant nutrition insights
                  </p>
                </div>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Button 
                    size="lg"
                    className="bg-primary hover:bg-primary-hover text-primary-foreground shadow-primary text-lg px-8 py-6 h-auto"
                  >
                    <Camera className="w-5 h-5 mr-3" />
                    Take Photo
                  </Button>
                  <Button 
                    variant="outline"
                    size="lg"
                    className="border-2 border-primary text-primary hover:bg-primary/10 transition-smooth text-lg px-8 py-6 h-auto"
                  >
                    <Upload className="w-5 h-5 mr-3" />
                    Upload Image
                  </Button>
                </div>
                <div className="text-sm text-muted-foreground">
                  Supports JPG, PNG, WebP • Max 10MB
                </div>
              </div>
            </div>
          ) : (
            <div className="grid lg:grid-cols-2 gap-0">
              <div className="p-8">
                <div className="relative mb-6">
                  <img
                    src={selectedImage}
                    alt="Selected meal"
                    className="w-full h-64 object-cover rounded-xl shadow-soft"
                  />
                </div>
                <div className="flex flex-col gap-3">
                  <Button
                    onClick={analyzeNutrition}
                    disabled={isAnalyzing}
                    size="lg"
                    className="bg-primary hover:bg-primary-hover text-primary-foreground shadow-primary w-full text-lg py-6 h-auto"
                  >
                    {isAnalyzing ? (
                      <Loader2 className="w-5 h-5 mr-3 animate-spin" />
                    ) : (
                      <Zap className="w-5 h-5 mr-3" />
                    )}
                    {isAnalyzing ? 'Analyzing...' : 'Analyze Nutrition'}
                  </Button>
                  <Button
                    onClick={resetAnalysis}
                    variant="outline"
                    size="lg"
                    className="border-border text-muted-foreground hover:bg-muted/50 transition-smooth w-full py-6 h-auto"
                  >
                    Take New Photo
                  </Button>
                </div>
              </div>
              
              {/* Preview Results Area */}
              <div className="bg-muted/30 p-8 flex items-center justify-center">
                {isAnalyzing ? (
                  <div className="text-center space-y-4">
                    <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto">
                      <Loader2 className="w-8 h-8 text-primary animate-spin" />
                    </div>
                    <div>
                      <div className="text-lg font-semibold text-foreground mb-2">
                        Analyzing your meal...
                      </div>
                      <div className="text-sm text-muted-foreground">
                        This usually takes less than 3 seconds
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="text-center text-muted-foreground">
                    <div className="text-lg mb-2">Ready to analyze!</div>
                    <div className="text-sm">Click "Analyze Nutrition" to get your results</div>
                  </div>
                )}
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Results Section */}
      {nutritionData && (
        <Card className="bg-gradient-card shadow-card border-border/50 animate-in slide-in-from-bottom duration-500">
          <CardContent className="p-8">
            <div className="text-center mb-6">
              <h3 className="text-2xl font-bold text-card-foreground mb-2">
                Nutrition Analysis
              </h3>
              <div className="w-16 h-1 bg-gradient-accent rounded mx-auto"></div>
            </div>
            
            {/* Total Nutrition */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
              <div className="text-center p-4 bg-primary/5 rounded-lg">
                <div className="text-3xl font-bold text-primary mb-1">
                  {nutritionData.totals.calories}
                </div>
                <div className="text-sm text-muted-foreground font-medium">
                  Calories
                </div>
              </div>
              
              <div className="text-center p-4 bg-secondary/5 rounded-lg">
                <div className="text-3xl font-bold text-secondary mb-1">
                  {nutritionData.totals.protein}g
                </div>
                <div className="text-sm text-muted-foreground font-medium">
                  Protein
                </div>
              </div>
              
              <div className="text-center p-4 bg-accent/5 rounded-lg">
                <div className="text-3xl font-bold text-accent mb-1">
                  {nutritionData.totals.carbs}g
                </div>
                <div className="text-sm text-muted-foreground font-medium">
                  Carbs
                </div>
              </div>
              
              <div className="text-center p-4 bg-muted rounded-lg">
                <div className="text-3xl font-bold text-card-foreground mb-1">
                  {nutritionData.totals.fat}g
                </div>
                <div className="text-sm text-muted-foreground font-medium">
                  Fat
                </div>
              </div>
            </div>

            {/* Food Items Breakdown */}
            <div className="space-y-4">
              <h4 className="text-lg font-semibold text-card-foreground mb-4">
                Food Items Detected
              </h4>
              <div className="space-y-3">
                {nutritionData.foods.map((item, index) => (
                  <div key={index} className="flex items-center justify-between p-4 bg-muted/30 rounded-lg">
                    <div className="flex-1">
                      <div className="font-medium text-card-foreground">{item.name}</div>
                      <div className="text-sm text-muted-foreground">{item.portion.value}{item.portion.unit}</div>
                    </div>
                    <div className="grid grid-cols-4 gap-3 text-sm text-right min-w-[200px]">
                      <div>
                        <div className="font-medium text-primary">{item.nutrition.calories}</div>
                        <div className="text-xs text-muted-foreground">cal</div>
                      </div>
                      <div>
                        <div className="font-medium text-secondary">{item.nutrition.protein}g</div>
                        <div className="text-xs text-muted-foreground">protein</div>
                      </div>
                      <div>
                        <div className="font-medium text-accent">{item.nutrition.carbs}g</div>
                        <div className="text-xs text-muted-foreground">carbs</div>
                      </div>
                      <div>
                        <div className="font-medium text-card-foreground">{item.nutrition.fat}g</div>
                        <div className="text-xs text-muted-foreground">fat</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="mt-6 p-4 bg-primary/5 rounded-lg">
              <p className="text-sm text-muted-foreground text-center">
                <span className="text-primary font-semibold">Powered by AI</span> • 
                Results are estimates based on visual analysis
              </p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};