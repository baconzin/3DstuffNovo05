import React, { useState, useEffect } from 'react';
import { Card, CardContent } from './ui/card';
import { Target, Lightbulb, Award, Heart, Loader2 } from 'lucide-react';
import { companyAPI } from '../services/api';

export const About = () => {
  const [companyInfo, setCompanyInfo] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCompanyInfo();
  }, []);

  const loadCompanyInfo = async () => {
    try {
      const data = await companyAPI.getInfo();
      setCompanyInfo(data);
    } catch (error) {
      console.error('Erro ao carregar informações da empresa:', error);
      // Fallback para dados padrão
      setCompanyInfo({
        name: "3D Stuff",
        about: "A 3D Stuff nasceu com a missão de transformar ideias em realidade através da impressão 3D. Trabalhamos com tecnologia de ponta e criatividade para oferecer peças únicas e personalizadas."
      });
    } finally {
      setLoading(false);
    }
  };

  const values = [
    {
      icon: Target,
      title: "Missão",
      description: "Transformar ideias em realidade através da impressão 3D de alta qualidade."
    },
    {
      icon: Lightbulb,
      title: "Inovação",
      description: "Utilizamos tecnologia de ponta para criar soluções únicas e criativas."
    },
    {
      icon: Award,
      title: "Qualidade",
      description: "Compromisso com a excelência em cada produto que desenvolvemos."
    },
    {
      icon: Heart,
      title: "Paixão",
      description: "Amor pelo que fazemos reflete em cada detalhe dos nossos produtos."
    }
  ];

  if (loading) {
    return (
      <section id="about" className="py-20 bg-gray-50">
        <div className="container mx-auto px-4 text-center">
          <Loader2 className="mx-auto h-12 w-12 animate-spin text-orange-500" />
          <p className="mt-4 text-gray-600">Carregando informações...</p>
        </div>
      </section>
    );
  }

  return (
    <section id="about" className="py-20 bg-gray-50">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Sobre a <span className="text-orange-500">{companyInfo?.name || "3D Stuff"}</span>
          </h2>
          <div className="max-w-3xl mx-auto">
            <p className="text-lg text-gray-600 leading-relaxed mb-8">
              {companyInfo?.about || "A 3D Stuff nasceu com a missão de transformar ideias em realidade através da impressão 3D."}
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
          {values.map((value, index) => {
            const IconComponent = value.icon;
            return (
              <Card 
                key={index}
                className="text-center p-6 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-2 border-0 shadow-md"
              >
                <CardContent className="p-0">
                  <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <IconComponent className="h-8 w-8 text-orange-500" />
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-3">
                    {value.title}
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    {value.description}
                  </p>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Stats Section */}
        <div className="bg-white rounded-2xl p-8 shadow-lg">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div className="p-6">
              <div className="text-4xl font-bold text-orange-500 mb-2">500+</div>
              <p className="text-gray-600 font-medium">Produtos Criados</p>
            </div>
            <div className="p-6">
              <div className="text-4xl font-bold text-orange-500 mb-2">100+</div>
              <p className="text-gray-600 font-medium">Clientes Satisfeitos</p>
            </div>
            <div className="p-6">
              <div className="text-4xl font-bold text-orange-500 mb-2">2+</div>
              <p className="text-gray-600 font-medium">Anos de Experiência</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};