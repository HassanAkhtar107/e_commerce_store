"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { FiBox, FiShoppingBag, FiClock, FiCheckCircle, FiUsers, FiTrendingUp } from "react-icons/fi";
import { api } from "@/Services/api";

const DEMO_STATS = {
  total_products: 12,
  total_orders: 8,
  pending_orders: 3,
  completed_orders: 5,
  total_customers: 24,
  recent_orders: [
    { id: 1, order_number: "ORD-98F2A10B", full_name: "Hassan Akhtar", total_amount: "2350", payment_method: "COD", order_status: "DELIVERED", created_at: "2026-09-21T12:00:00Z" },
    { id: 2, order_number: "ORD-41B9C78E", full_name: "Ayesha Khan", total_amount: "1450", payment_method: "COD", order_status: "PENDING", created_at: "2026-09-21T14:30:00Z" }
  ]
};

export default function AdminDashboardPage() {
  const [stats, setStats] = useState(DEMO_STATS);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      setLoading(true);
      const data = await api.getDashboardStats();
      if (data && data.total_products !== undefined) {
        setStats(data);
      }
    } catch (err) {
      console.warn("Using demo stats for admin dashboard", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
        <div>
          <span className="text-xs font-bold text-blue-400 uppercase tracking-widest">Admin Control Portal</span>
          <h1 className="text-3xl font-black text-white">Store Overview Dashboard</h1>
        </div>
        
        <a
          href="/admin"
          target="_blank"
          rel="noopener noreferrer"
          className="px-5 py-2.5 rounded-xl text-xs font-bold text-white btn-gradient flex items-center gap-2 shadow-lg shadow-blue-500/25"
        >
          <span>Django Admin Panel</span>
          <FiTrendingUp />
        </a>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6 mb-12">
        
        <div className="glass-card rounded-3xl p-6 border border-slate-800 space-y-2">
          <div className="w-10 h-10 rounded-xl bg-blue-500/10 text-blue-400 flex items-center justify-center text-xl">
            <FiBox />
          </div>
          <span className="text-xs text-slate-400 font-semibold block">Total Products</span>
          <span className="text-3xl font-black text-white">{stats.total_products}</span>
        </div>

        <div className="glass-card rounded-3xl p-6 border border-slate-800 space-y-2">
          <div className="w-10 h-10 rounded-xl bg-purple-500/10 text-purple-400 flex items-center justify-center text-xl">
            <FiShoppingBag />
          </div>
          <span className="text-xs text-slate-400 font-semibold block">Total Orders</span>
          <span className="text-3xl font-black text-white">{stats.total_orders}</span>
        </div>

        <div className="glass-card rounded-3xl p-6 border border-slate-800 space-y-2">
          <div className="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center text-xl">
            <FiClock />
          </div>
          <span className="text-xs text-slate-400 font-semibold block">Pending Orders</span>
          <span className="text-3xl font-black text-amber-400">{stats.pending_orders}</span>
        </div>

        <div className="glass-card rounded-3xl p-6 border border-slate-800 space-y-2">
          <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center text-xl">
            <FiCheckCircle />
          </div>
          <span className="text-xs text-slate-400 font-semibold block">Completed</span>
          <span className="text-3xl font-black text-emerald-400">{stats.completed_orders}</span>
        </div>

        <div className="glass-card rounded-3xl p-6 border border-slate-800 space-y-2">
          <div className="w-10 h-10 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center text-xl">
            <FiUsers />
          </div>
          <span className="text-xs text-slate-400 font-semibold block">Registered Users</span>
          <span className="text-3xl font-black text-white">{stats.total_customers}</span>
        </div>

      </div>

      {/* Recent Orders Table */}
      <div className="glass-card rounded-3xl p-6 border border-slate-800 space-y-6">
        <h2 className="text-lg font-bold text-white">Recent Orders</h2>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-900/80 text-slate-400 uppercase tracking-wider text-[10px] border-b border-slate-800">
              <tr>
                <th className="py-3 px-4">Order ID</th>
                <th className="py-3 px-4">Customer</th>
                <th className="py-3 px-4">Payment</th>
                <th className="py-3 px-4">Total</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {stats.recent_orders?.map((ord) => (
                <tr key={ord.id} className="hover:bg-slate-900/40">
                  <td className="py-3.5 px-4 font-bold text-white">{ord.order_number}</td>
                  <td className="py-3.5 px-4">{ord.full_name || "Guest Customer"}</td>
                  <td className="py-3.5 px-4 font-semibold text-blue-400">{ord.payment_method || "COD"}</td>
                  <td className="py-3.5 px-4 font-extrabold text-white">Rs. {Number(ord.total_amount).toLocaleString()}</td>
                  <td className="py-3.5 px-4">
                    <span className={`px-2.5 py-1 rounded-full font-extrabold text-[10px] ${
                      ord.order_status === "DELIVERED" ? "bg-emerald-500/20 text-emerald-400" : "bg-amber-500/20 text-amber-400"
                    }`}>
                      {ord.order_status}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-slate-500">{new Date(ord.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}
