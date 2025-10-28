import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { ShoppingCart, Eye, Filter, Loader2 } from 'lucide-react';
import { productsAPI } from '../services/api';
import { useToast } from '../hooks/use-toast';
import { PaymentModal } from './PaymentModal';

export const Products = () => {
  const [products, setProducts] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('Todos');
  const [loading, setLoading] = useState(true);
  const [categories, setCategories] = useState(['Todos']);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [isPaymentModalOpen, setIsPaymentModalOpen] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    loadProducts();
  }, [selectedCategory]);

  const loadProducts = async () => {
    try {
      setLoading(true);
      const data = await productsAPI.getAll(selectedCategory);
      setProducts(data);
      
      // Extrair categorias únicas
      if (selectedCategory === 'Todos') {
        const uniqueCategories = ['Todos', ...new Set(data.map(product => product.category))];
        setCategories(uniqueCategories);
      }
    } catch (error) {
      console.error('Erro ao carregar produtos:', error);
      toast({
        title: "Erro",
        description: "Não foi possível carregar os produtos. Tente novamente.",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const handleBuyClick = (product) => {
    setSelectedProduct(product);
    setIsPaymentModalOpen(true);
  };

  const handlePaymentSuccess = (paymentData) => {
    toast({
      title: "🎉 Pagamento realizado!",
      description: `Compra de "${selectedProduct.name}" finalizada com sucesso!`,
    });
    setIsPaymentModalOpen(false);
    setSelectedProduct(null);
  };

  const handleViewMore = (product) => {
    // Mock para visualizar mais detalhes
    toast({
      title: "Detalhes do produto",
      description: `Visualizando "${product.name}". Funcionalidade de detalhes completos será implementada em breve.`,
    });
  };

  if (loading) {
    return (
      <section id="products" className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <Loader2 className="mx-auto h-12 w-12 animate-spin text-blue-500" />
            <p className="mt-4 text-gray-600">Carregando produtos...</p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section id="products" className="py-20 bg-white">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Nossos <span className="text-blue-500">Produtos</span>
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Descubra nossa coleção exclusiva de produtos em impressão 3D, 
            cada um criado com precisão e qualidade excepcional.
          </p>
        </div>

        {/* Category Filter */}
        <div className="flex flex-wrap justify-center gap-4 mb-12">
          <div className="flex items-center gap-2 mb-4">
            <Filter className="h-5 w-5 text-gray-500" />
            <span className="text-gray-700 font-medium">Filtrar por:</span>
          </div>
          {categories.map((category) => (
            <Button
              key={category}
              variant={selectedCategory === category ? "default" : "outline"}
              onClick={() => setSelectedCategory(category)}
              className={`transition-all duration-200 ${
                selectedCategory === category 
                  ? 'bg-blue-500 hover:bg-blue-600 text-white' 
                  : 'hover:border-blue-500 hover:text-blue-500'
              }`}
            >
              {category}
            </Button>
          ))}
        </div>

        {/* Products Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {products.map((product) => (
            <Card 
              key={product.id} 
              className="group hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2 border-0 shadow-md overflow-hidden"
            >
              <CardHeader className="p-0">
                <div className="relative overflow-hidden">
                  <img
                    src={product.image}
                    alt={product.name}
                    className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-110"
                  />
                  <div className="absolute top-4 right-4">
                    <Badge variant="secondary" className="bg-white/90 text-gray-700">
                      {product.category}
                    </Badge>
                  </div>
                </div>
              </CardHeader>

              <CardContent className="p-6">
                <CardTitle className="text-xl font-bold text-gray-900 mb-3 group-hover:text-blue-500 transition-colors">
                  {product.name}
                </CardTitle>
                <p className="text-gray-600 mb-4 leading-relaxed">
                  {product.description}
                </p>
                <div className="flex items-center justify-between">
                  <span className="text-2xl font-bold text-blue-500">
                    {product.price}
                  </span>
                </div>
              </CardContent>

              <CardFooter className="p-6 pt-0 flex gap-3">
                <Button 
                  onClick={() => handleBuyClick(product)}
                  className="flex-1 bg-blue-500 hover:bg-blue-600 text-white transition-all duration-200 transform hover:scale-105"
                >
                  <ShoppingCart className="mr-2 h-4 w-4" />
                  Comprar
                </Button>
                <Button 
                  variant="outline" 
                  onClick={() => handleViewMore(product)}
                  className="hover:border-blue-500 hover:text-blue-500 transition-all duration-200"
                >
                  <Eye className="h-4 w-4" />
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>

        {products.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">
              Nenhum produto encontrado para a categoria selecionada.
            </p>
          </div>
        )}

        {/* Payment Modal */}
        <PaymentModal
          product={selectedProduct}
          isOpen={isPaymentModalOpen}
          onClose={() => {
            setIsPaymentModalOpen(false);
            setSelectedProduct(null);
          }}
          onSuccess={handlePaymentSuccess}
        />
      </div>
    </section>
  );
};