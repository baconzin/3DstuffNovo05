import React from 'react';

// Logo 3D Stuff em SVG - Versão adaptada para as cores do site
export const Logo3DStuff = ({ className = "h-8 w-8", variant = "orange" }) => {
  const colors = {
    orange: {
      primary: "#f97316",   // Laranja principal
      secondary: "#fb923c", // Laranja claro
      accent: "#ea580c"     // Laranja escuro
    },
    white: {
      primary: "#ffffff",
      secondary: "#f9fafb",
      accent: "#e5e7eb"
    },
    dark: {
      primary: "#1f2937",
      secondary: "#374151",
      accent: "#111827"
    }
  };

  const currentColors = colors[variant] || colors.orange;

  return (
    <svg
      className={className}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Engrenagem exterior - Laranja */}
      <path
        d="M50 10L55 15L60 10L65 15L70 10L75 15L80 20L75 25L80 30L75 35L80 40L75 45L80 50L75 55L80 60L75 65L80 70L75 75L70 80L65 75L60 80L55 75L50 80L45 75L40 80L35 75L30 80L25 75L20 70L25 65L20 60L25 55L20 50L25 45L20 40L25 35L20 30L25 25L20 20L25 15L30 10L35 15L40 10L45 15L50 10Z"
        fill={currentColors.primary}
        stroke={currentColors.accent}
        strokeWidth="1"
      />
      
      {/* Cubo 3D central - Gradiente */}
      <defs>
        <linearGradient id="cubeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor={currentColors.secondary} />
          <stop offset="100%" stopColor={currentColors.accent} />
        </linearGradient>
      </defs>
      
      {/* Face frontal do cubo */}
      <path
        d="M35 35L65 35L65 65L35 65Z"
        fill="url(#cubeGradient)"
        stroke={currentColors.accent}
        strokeWidth="2"
      />
      
      {/* Face superior do cubo (perspectiva 3D) */}
      <path
        d="M35 35L45 25L75 25L65 35Z"
        fill={currentColors.secondary}
        stroke={currentColors.accent}
        strokeWidth="2"
      />
      
      {/* Face lateral do cubo (perspectiva 3D) */}
      <path
        d="M65 35L75 25L75 55L65 65Z"
        fill={currentColors.primary}
        stroke={currentColors.accent}
        strokeWidth="2"
      />
      
      {/* Detalhes internos da engrenagem */}
      <circle
        cx="50"
        cy="50"
        r="8"
        fill="none"
        stroke={currentColors.accent}
        strokeWidth="2"
      />
    </svg>
  );
};

// Versão simplificada para uso em botões pequenos
export const Logo3DStuffSimple = ({ className = "h-6 w-6", color = "#f97316" }) => {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Engrenagem simplificada */}
      <path
        d="M12 2L13.5 3.5L15 2L16.5 3.5L18 2L19.5 3.5L21 5L19.5 6.5L21 8L19.5 9.5L21 11L19.5 12.5L21 14L19.5 15.5L21 17L19.5 18.5L18 20L16.5 18.5L15 20L13.5 18.5L12 20L10.5 18.5L9 20L7.5 18.5L6 20L4.5 18.5L3 17L4.5 15.5L3 14L4.5 12.5L3 11L4.5 9.5L3 8L4.5 6.5L3 5L4.5 3.5L6 2L7.5 3.5L9 2L10.5 3.5L12 2Z"
        fill={color}
        fillOpacity="0.2"
        stroke={color}
        strokeWidth="1"
      />
      
      {/* Cubo central */}
      <path
        d="M8 8L16 8L16 16L8 16Z"
        fill={color}
        stroke="white"
        strokeWidth="1.5"
      />
      
      {/* Face 3D */}
      <path
        d="M8 8L10 6L18 6L16 8Z"
        fill={color}
        fillOpacity="0.8"
      />
      
      <path
        d="M16 8L18 6L18 14L16 16Z"
        fill={color}
        fillOpacity="0.6"
      />
    </svg>
  );
};

// Logo completo com texto para header
export const Logo3DStuffComplete = ({ className = "", variant = "orange" }) => {
  return (
    <div className={`flex items-center space-x-3 ${className}`}>
      <Logo3DStuff variant={variant} className="h-10 w-10" />
      <div className="flex flex-col">
        <span className="text-2xl font-bold text-gray-900">3D STUFF</span>
        <span className="text-xs text-gray-600 -mt-1">Impressão 3D</span>
      </div>
    </div>
  );
};

// Logo para footer (versão branca)
export const Logo3DStuffFooter = ({ className = "" }) => {
  return (
    <div className={`flex items-center space-x-3 ${className}`}>
      <Logo3DStuff variant="white" className="h-8 w-8" />
      <span className="text-2xl font-bold text-white">3D STUFF</span>
    </div>
  );
};