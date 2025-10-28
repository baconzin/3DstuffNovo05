import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Header } from "./components/Header";
import { Hero } from "./components/Hero";
import { Products } from "./components/Products";
import { About } from "./components/About";
import { Contact } from "./components/Contact";
import { Footer } from "./components/Footer";
import { WhatsAppFloat } from "./components/WhatsAppFloat";
import { Toaster } from "./components/ui/sonner";

const Home = () => {
  return (
    <>
      <Header />
      <main>
        <Hero />
        <Products />
        <About />
        <Contact />
      </main>
      <Footer />
      
      {/* Apenas o ícone flutuante pequeno */}
      <WhatsAppFloat />
      
      <Toaster />
    </>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;