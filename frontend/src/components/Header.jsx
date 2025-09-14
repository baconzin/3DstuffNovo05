import React, { useState } from 'react';
import { Button } from './ui/button';
import { Menu, X } from 'lucide-react';
import { Logo3DStuffComplete } from './Logo';

export const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
    setIsMenuOpen(false);
  };

  return (
    <header className="fixed top-0 left-0 right-0 bg-white/95 backdrop-blur-sm z-50 border-b border-gray-100">
      <nav className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Logo3DStuffComplete variant="orange" />

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <button 
              onClick={() => scrollToSection('home')}
              className="text-gray-700 hover:text-orange-500 transition-colors duration-200"
            >
              Início
            </button>
            <button 
              onClick={() => scrollToSection('products')}
              className="text-gray-700 hover:text-orange-500 transition-colors duration-200"
            >
              Produtos
            </button>
            <button 
              onClick={() => scrollToSection('about')}
              className="text-gray-700 hover:text-orange-500 transition-colors duration-200"
            >
              Sobre
            </button>
            <button 
              onClick={() => scrollToSection('contact')}
              className="text-gray-700 hover:text-orange-500 transition-colors duration-200"
            >
              Contato
            </button>
            <Button 
              onClick={() => scrollToSection('products')}
              className="bg-orange-500 hover:bg-orange-600 text-white transition-all duration-200 transform hover:scale-105"
            >
              Ver Produtos
            </Button>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden p-2 text-gray-700 hover:text-orange-500 transition-colors"
          >
            {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden mt-4 py-4 border-t border-gray-100">
            <div className="flex flex-col space-y-4">
              <button 
                onClick={() => scrollToSection('home')}
                className="text-left text-gray-700 hover:text-orange-500 transition-colors duration-200"
              >
                Início
              </button>
              <button 
                onClick={() => scrollToSection('products')}
                className="text-left text-gray-700 hover:text-orange-500 transition-colors duration-200"
              >
                Produtos
              </button>
              <button 
                onClick={() => scrollToSection('about')}
                className="text-left text-gray-700 hover:text-orange-500 transition-colors duration-200"
              >
                Sobre
              </button>
              <button 
                onClick={() => scrollToSection('contact')}
                className="text-left text-gray-700 hover:text-orange-500 transition-colors duration-200"
              >
                Contato
              </button>
              <Button 
                onClick={() => scrollToSection('products')}
                className="bg-orange-500 hover:bg-orange-600 text-white w-fit"
              >
                Ver Produtos
              </Button>
            </div>
          </div>
        )}
      </nav>
    </header>
  );
};