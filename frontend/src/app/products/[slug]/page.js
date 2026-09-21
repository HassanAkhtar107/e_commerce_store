"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { FiStar, FiShoppingBag, FiTruck, FiShield, FiRefreshCw, FiPlus, FiMinus, FiCheck } from "react-icons/fi";
import { useCart } from "@/context/CartContext";
import { api } from "@/Services/api";

const DEMO_PRODUCT = {
  id: 1,
  name: "Nexus Pro Wireless Headphones",
  slug: "nexus-pro-wireless-headphones",
  category: "Electronics",
  brand: "Nexus Audio",
  price: 199.99,
  discount_price: 149.99,
  stock: 25,
  rating: 4.8,
  num_reviews: 32,
  description: "Experience pure audio immersion with the Nexus Pro Wireless Headphones. Equipped with hybrid Active Noise Cancellation (ANC), 40mm custom drivers, and up to 40 hours of continuous playback.",
  short_description: "Premium ANC wireless headphones with studio clarity.",
  images: [
    { image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80" },
    { image: "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=800&auto=format&fit=crop&q=80" }
  ],
  reviews: [
    { id: 1, user_name: "Alex M.", rating: 5, comment: "Exceptional sound quality and ANC is top tier! Battery lasts all week.", created_at: "2026-02-10" },
    { id: 2, user_name: "Sarah K.", rating: 5, comment: "Super comfortable for long work hours and flights.", created_at: "2026-02-14" }
  ]
};

export default function ProductDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { addToCart } = useCart();

  const [product, setProduct] = useState(DEMO_PRODUCT);
  const [selectedImage, setSelectedImage] = useState("");
  const [quantity, setQuantity] = useState(1);
  const [loading, setLoading] = useState(true);
  const [added, setAdded] = useState(false);

  useEffect(() => {
    if (params?.slug) {
      fetchProduct(params.slug);
    }
  }, [params?.slug]);

  const fetchProduct = async (slug) => {
    try {
      setLoading(true);
      const data = await api.getProductBySlug(slug);
      if (data && data.name) {
        setProduct(data);
        if (data.images && data.images.length > 0) {
          setSelectedImage(data.images[0].image);
        }
      }
    } catch (err) {
      console.warn("Using demo product detail fallback", err);
      setSelectedImage(DEMO_PRODUCT.images[0].image);
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = () => {
    addToCart(product, quantity);
    setAdded(true);
    setTimeout(() => setAdded(false), 2000);
  };

  const price = Number(product.price || 0);
  const discountPrice = product.discount_price ? Number(product.discount_price) : null;
  const currentPrice = discountPrice || price;
  const mainImg = selectedImage || (product.images?.[0]?.image) || "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80";

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      
      {/* Breadcrumb */}
      <div className="text-xs text-slate-400 mb-8 flex items-center gap-2">
        <span onClick={() => router.push("/")} className="hover:text-white cursor-pointer">Home</span>
        <span>/</span>
        <span onClick={() => router.push("/products")} className="hover:text-white cursor-pointer">Products</span>
        <span>/</span>
        <span className="text-blue-400 font-semibold">{product.name}</span>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 mb-16">
        
        {/* Left: Gallery */}
        <div className="space-y-4">
          <div className="glass-card rounded-3xl p-4 overflow-hidden relative aspect-square bg-slate-900 border border-slate-800">
            <img
              src={mainImg}
              alt={product.name}
              className="w-full h-full object-cover rounded-2xl"
            />
          </div>

          {product.images && product.images.length > 1 && (
            <div className="flex gap-4 overflow-x-auto pb-2">
              {product.images.map((img, idx) => (
                <button
                  key={idx}
                  onClick={() => setSelectedImage(img.image)}
                  className={`w-20 h-20 rounded-xl overflow-hidden border-2 transition-all shrink-0 ${
                    selectedImage === img.image ? "border-blue-500 scale-105" : "border-slate-800 opacity-60 hover:opacity-100"
                  }`}
                >
                  <img src={img.image} alt="" className="w-full h-full object-cover" />
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Right: Details */}
        <div className="space-y-6">
          
          <div>
            <div className="flex items-center gap-3 text-xs mb-2">
              <span className="px-2.5 py-1 rounded-full bg-blue-500/10 text-blue-400 font-bold border border-blue-500/20">
                {product.category_detail?.name || product.category || "General"}
              </span>
              <span className="text-slate-400 font-semibold">{product.brand_detail?.name || product.brand}</span>
            </div>
            
            <h1 className="text-3xl sm:text-4xl font-black text-white">{product.name}</h1>

            {/* Rating */}
            <div className="flex items-center gap-2 mt-3 text-xs text-slate-400">
              <div className="flex text-amber-400">
                {[...Array(5)].map((_, i) => (
                  <FiStar key={i} className="fill-amber-400" />
                ))}
              </div>
              <span className="font-bold text-slate-200">{product.rating}</span>
              <span>({product.num_reviews} customer reviews)</span>
            </div>
          </div>

          {/* Price Tag */}
          <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 flex items-center gap-4">
            <span className="text-3xl font-black text-white">${currentPrice.toFixed(2)}</span>
            {discountPrice && (
              <span className="text-lg text-slate-500 line-through">${price.toFixed(2)}</span>
            )}
            {discountPrice && (
              <span className="text-xs bg-red-500/20 text-red-400 font-bold px-2.5 py-1 rounded-full border border-red-500/30">
                Save ${(price - discountPrice).toFixed(2)}
              </span>
            )}
          </div>

          <p className="text-slate-300 text-sm leading-relaxed">{product.description}</p>

          {/* Quantity and Add to Cart */}
          <div className="pt-4 border-t border-slate-800 space-y-4">
            <div className="flex items-center gap-4">
              <span className="text-xs font-bold text-slate-400">Quantity</span>
              <div className="flex items-center border border-slate-700 rounded-xl bg-slate-900">
                <button
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  className="p-2.5 hover:text-blue-400"
                >
                  <FiMinus />
                </button>
                <span className="px-4 font-bold text-sm">{quantity}</span>
                <button
                  onClick={() => setQuantity(quantity + 1)}
                  className="p-2.5 hover:text-blue-400"
                >
                  <FiPlus />
                </button>
              </div>
              <span className="text-xs text-emerald-400 font-semibold">
                In Stock ({product.stock} available)
              </span>
            </div>

            <div className="flex gap-4">
              <button
                onClick={handleAddToCart}
                className={`flex-1 py-4 px-6 rounded-xl font-bold text-sm flex items-center justify-center gap-2 shadow-xl transition-all ${
                  added
                    ? "bg-emerald-600 text-white"
                    : "btn-gradient text-white shadow-blue-500/25"
                }`}
              >
                {added ? <FiCheck className="text-lg" /> : <FiShoppingBag className="text-lg" />}
                <span>{added ? "Added to Cart!" : "Add to Shopping Cart"}</span>
              </button>
            </div>
          </div>

          {/* Guarantees */}
          <div className="grid grid-cols-3 gap-3 pt-4 border-t border-slate-800 text-center">
            <div className="p-3 rounded-xl bg-slate-900/50 border border-slate-800">
              <FiTruck className="text-lg text-blue-400 mx-auto mb-1" />
              <span className="text-[10px] font-semibold text-slate-300 block">Express Delivery</span>
            </div>
            <div className="p-3 rounded-xl bg-slate-900/50 border border-slate-800">
              <FiShield className="text-lg text-indigo-400 mx-auto mb-1" />
              <span className="text-[10px] font-semibold text-slate-300 block">2 Year Warranty</span>
            </div>
            <div className="p-3 rounded-xl bg-slate-900/50 border border-slate-800">
              <FiRefreshCw className="text-lg text-purple-400 mx-auto mb-1" />
              <span className="text-[10px] font-semibold text-slate-300 block">30 Day Returns</span>
            </div>
          </div>

        </div>

      </div>

      {/* Customer Reviews Section */}
      <div className="glass-card rounded-3xl p-8 border border-slate-800">
        <h3 className="text-xl font-bold text-white mb-6">Customer Reviews</h3>
        
        {product.reviews && product.reviews.length > 0 ? (
          <div className="space-y-4">
            {product.reviews.map((rev) => (
              <div key={rev.id} className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80">
                <div className="flex justify-between items-center mb-2">
                  <span className="font-bold text-sm text-slate-200">{rev.user_name}</span>
                  <div className="flex text-amber-400 text-xs">
                    {[...Array(rev.rating)].map((_, i) => (
                      <FiStar key={i} className="fill-amber-400" />
                    ))}
                  </div>
                </div>
                <p className="text-xs text-slate-400">{rev.comment}</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-500">No reviews yet for this product.</p>
        )}
      </div>

    </div>
  );
}
