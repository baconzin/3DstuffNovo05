import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { ShoppingCart, Eye, Filter } from 'lucide-react';
import { products } from '../mock';

export const Products = () => {
  const [selectedCategory, setSelectedCategory] = useState('Todos');
  
  const categories = ['Todos', ...new Set(products.map(product => product.category))];
  
  const filteredProducts = selectedCategory === 'Todos' 
    ? products 
    : products.filter(product => product.category === selectedCategory);

  const handleBuyClick = (product) => {
    // Mock da funcionalidade de compra - será implementada no backend
    alert(`Produto "${product.name}" adicionado ao carrinho! (Funcionalidade será implementada)`);
  };

  const handleViewMore = (product) => {
    // Mock para visualizar mais detalhes
    alert(`Visualizando detalhes de "${product.name}" (Será implementado)`);
  };

  return (
    <section id="products" className="py-20 bg-white">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Nossos <span className="text-orange-500">Produtos</span>
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
                  ? 'bg-orange-500 hover:bg-orange-600 text-white' 
                  : 'hover:border-orange-500 hover:text-orange-500'
              }`}
            >
              {category}
            </Button>
          ))}
        </div>

        {/* Products Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {filteredProducts.map((product) => (
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
                <CardTitle className="text-xl font-bold text-gray-900 mb-3 group-hover:text-orange-500 transition-colors">
                  {product.name}
                </CardTitle>
                <p className="text-gray-600 mb-4 leading-relaxed">
                  {product.description}
                </p>
                <div className="flex items-center justify-between">
                  <span className="text-2xl font-bold text-orange-500">
                    {product.price}
                  </span>
                </div>
              </CardContent>

              <CardFooter className="p-6 pt-0 flex gap-3">
                <Button 
                  onClick={() => handleBuyClick(product)}
                  className="flex-1 bg-orange-500 hover:bg-orange-600 text-white transition-all duration-200 transform hover:scale-105"
                >
                  <ShoppingCart className="mr-2 h-4 w-4" />
                  Comprar
                </Button>
                <Button 
                  variant="outline" 
                  onClick={() => handleViewMore(product)}
                  className="hover:border-orange-500 hover:text-orange-500 transition-all duration-200"
                >
                  <Eye className="h-4 w-4" />
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>

        {filteredProducts.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">
              Nenhum produto encontrado para a categoria selecionada.
            </p>
          </div>
        )}
      </div>
    </section>
  );
};