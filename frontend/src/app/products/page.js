"use client";

import React, { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import ProductCard from "@/components/ProductCard";
import { api } from "@/Services/api";
import { FiSearch, FiSliders, FiX } from "react-icons/fi";

const INITIAL_PRODUCTS = [
  {
    id: 1,
    name: "Nexus Pro Wireless Headphones",
    slug: "nexus-pro-wireless-headphones",
    category: "electronics",
    price: 199.99,
    discount_price: 149.99,
    rating: 4.8,
    num_reviews: 32,
    images: [{ image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80" }]
  },
  {
    id: 2,
    name: "Urban Minimalist Bomber Jacket",
    slug: "urban-minimalist-bomber-jacket",
    category: "fashion-apparel",
    price: 129.00,
    discount_price: 89.00,
    rating: 4.6,
    num_reviews: 19,
    images: [{ image: "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&auto=format&fit=crop&q=80" }]
  },
  {
    id: 3,
    name: "Luxe Ambient Ceramic Desk Lamp",
    slug: "luxe-ambient-ceramic-desk-lamp",
    category: "home-lifestyle",
    price: 89.50,
    rating: 4.9,
    num_reviews: 14,
    images: [{ image: "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&auto=format&fit=crop&q=80" }]
  },
  {
    id: 4,
    name: "Smart Fitness Watch Ultra",
    slug: "smart-fitness-watch-ultra",
    category: "sports-fitness",
    price: 249.99,
    discount_price: 199.99,
    rating: 4.7,
    num_reviews: 45,
    images: [{ image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80" }]
  },
  {
    id: 5,
    name: "Retro Leather Sneakers",
    slug: "retro-leather-sneakers",
    category: "fashion-apparel",
    price: 110.00,
    discount_price: 95.00,
    rating: 4.5,
    num_reviews: 22,
    images: [{ image: "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=800&auto=format&fit=crop&q=80" }]
  },
  {
    id: 6,
    name: "Aroma Espresso Machine Pro",
    slug: "aroma-espresso-machine-pro",
    category: "home-lifestyle",
    price: 349.00,
    discount_price: 299.00,
    rating: 4.9,
    num_reviews: 28,
    images: [{ image: "https://images.unsplash.com/photo-1517668808822-9e428d697818?w=800&auto=format&fit=crop&q=80" }]
  }
];

function ProductsContent() {
  const searchParams = useSearchParams();
  const initialCategory = searchParams.get("category") || "all";
  const initialSearch = searchParams.get("search") || "";

  const [products, setProducts] = useState(INITIAL_PRODUCTS);
  const [selectedCategory, setSelectedCategory] = useState(initialCategory);
  const [searchQuery, setSearchQuery] = useState(initialSearch);
  const [sortBy, setSortBy] = useState("default");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProducts();
  }, [selectedCategory, searchQuery, sortBy]);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      let queryParams = [];
      if (selectedCategory !== "all") queryParams.push(`category__slug=${selectedCategory}`);
      if (searchQuery) queryParams.push(`search=${encodeURIComponent(searchQuery)}`);
      if (sortBy === "price-low") queryParams.push("ordering=price");
      if (sortBy === "price-high") queryParams.push("ordering=-price");

      const queryStr = queryParams.length > 0 ? `?${queryParams.join("&")}` : "";
      const data = await api.getProducts(queryStr);
      if (data && data.results && data.results.length > 0) {
        setProducts(data.results);
      } else if (Array.isArray(data) && data.length > 0) {
        setProducts(data);
      }
    } catch (err) {
      console.warn("API unavailable, filtering local demo products", err);
    } finally {
      setLoading(false);
    }
  };

  // Local filtering fallback
  const filteredProducts = products.filter((p) => {
    const matchesCat = selectedCategory === "all" || (p.category && p.category.toLowerCase().includes(selectedCategory.toLowerCase()));
    const matchesQuery = !searchQuery || p.name.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCat && matchesQuery;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      
      {/* Page Header */}
      <div className="mb-10 text-center sm:text-left">
        <h1 className="text-4xl font-black text-white">Explore Products</h1>
        <p className="text-slate-400 text-sm mt-1">Discover curated items with guaranteed quality and fast delivery.</p>
      </div>

      {/* Filter Controls Bar */}
      <div className="glass-card rounded-2xl p-4 mb-10 flex flex-col md:flex-row items-center justify-between gap-4">
        
        {/* Search Input */}
        <div className="relative w-full md:w-80">
          <input
            type="text"
            placeholder="Search products..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700/80 rounded-xl px-4 py-2.5 pl-10 text-sm text-slate-200 focus:outline-none focus:border-blue-500"
          />
          <FiSearch className="absolute left-3.5 top-3 text-slate-400" />
          {searchQuery && (
            <button onClick={() => setSearchQuery("")} className="absolute right-3 top-3 text-slate-400 hover:text-white">
              <FiX />
            </button>
          )}
        </div>

        {/* Category Pills */}
        <div className="flex items-center gap-2 overflow-x-auto w-full md:w-auto pb-2 md:pb-0 scrollbar-none">
          {[
            { label: "All Items", value: "all" },
            { label: "Electronics", value: "electronics" },
            { label: "Fashion", value: "fashion-apparel" },
            { label: "Home", value: "home-lifestyle" },
            { label: "Fitness", value: "sports-fitness" },
          ].map((cat) => (
            <button
              key={cat.value}
              onClick={() => setSelectedCategory(cat.value)}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition-all whitespace-nowrap ${
                selectedCategory === cat.value
                  ? "bg-blue-600 text-white shadow-lg shadow-blue-500/25"
                  : "bg-slate-900/80 text-slate-400 hover:text-white hover:bg-slate-800"
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>

        {/* Sort Select */}
        <div className="flex items-center gap-2 w-full md:w-auto">
          <FiSliders className="text-slate-400 text-sm" />
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-slate-300 text-xs rounded-xl px-3 py-2.5 focus:outline-none focus:border-blue-500"
          >
            <option value="default">Sort by: Featured</option>
            <option value="price-low">Price: Low to High</option>
            <option value="price-high">Price: High to Low</option>
          </select>
        </div>

      </div>

      {/* Product Grid */}
      {filteredProducts.length === 0 ? (
        <div className="text-center py-24 glass-card rounded-2xl">
          <FiSearch className="text-5xl text-slate-600 mx-auto mb-4" />
          <h3 className="text-lg font-bold text-slate-200">No products found</h3>
          <p className="text-xs text-slate-400 mt-1">Try clearing your filters or searching for something else.</p>
          <button
            onClick={() => { setSelectedCategory("all"); setSearchQuery(""); }}
            className="mt-4 px-4 py-2 bg-blue-600 text-white text-xs font-bold rounded-xl"
          >
            Reset Filters
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredProducts.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      )}

    </div>
  );
}

export default function ProductsPage() {
  return (
    <Suspense fallback={<div className="text-center py-20 text-slate-400">Loading catalog...</div>}>
      <ProductsContent />
    </Suspense>
  );
}
