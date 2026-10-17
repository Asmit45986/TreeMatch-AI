'use client';

import React, { useState } from 'react';
import axios from 'axios';
import { Upload, TreePine, Sprout, DollarSign, Cloud, ShieldCheck, Loader2, AlertCircle, Layers, TrendingUp } from 'lucide-react';

interface StressMatrix {
  ph_status: string;
  thermal_risk: string;
  aqi_impact: string;
}

interface RoiScenarios {
  conservative_usd: number;
  expected_usd: number;
  optimistic_usd: number;
}

interface PredictionResponse {
  predicted_soil_type: string;
  recommended_tree: string;
  survival_probability: number;
  carbon_offset_tons_per_year: number;
  financial_roi_estimate_usd: number;
  maturation_years: number;
  stress_matrix: StressMatrix;
  roi_scenarios: RoiScenarios;
  soil_advisory: string;
  alternative_species: string[];
  message: string;
}

export default function Home() {
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [telemetry, setTelemetry] = useState({
    Land_Type: 'Agricultural',
    pH: 6.5,
    Rainfall: 800,
    Temperature: 25,
    Humidity: 60,
    Nitrogen: 40,
    Phosphorus: 30,
    Potassium: 20,
    Elevation: 200,
    Organic_Carbon: 0.5,
    Moisture: 45,
    Vegetation_Percentage: 30,
    Water_Nearby: 1,
    AQI: 80,
  });

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setImageFile(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!imageFile) {
      setError('Please upload a soil image first.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', imageFile);
      Object.entries(telemetry).forEach(([key, value]) => {
        formData.append(key, value.toString());
      });

      const response = await axios.post<PredictionResponse>(
        'http://127.0.0.1:8000/api/v1/predict',
        formData,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );

      setResult(response.data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to connect to backend server.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-6 md:p-12">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Header */}
        <header className="flex items-center space-x-3 border-b border-slate-800 pb-6">
          <TreePine className="h-10 w-10 text-emerald-400" />
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white">GreenMind AI Platform</h1>
            <p className="text-sm text-slate-400">Afforestation Intelligence & Multi-Scenario Carbon Analysis System</p>
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Input Form (5 cols) */}
          <form onSubmit={handleSubmit} className="lg:col-span-5 bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
            <h2 className="text-xl font-semibold text-emerald-400 flex items-center gap-2">
              <Upload className="h-5 w-5" /> Input Soil Image & Environmental Telemetry
            </h2>

            {/* Image Upload Area */}
            <div className="border-2 border-dashed border-slate-700 hover:border-emerald-500 transition rounded-lg p-4 text-center">
              <input type="file" accept="image/*" onChange={handleImageChange} className="hidden" id="soil-image-input" />
              <label htmlFor="soil-image-input" className="cursor-pointer block space-y-2">
                {previewUrl ? (
                  <img src={previewUrl} alt="Soil Sample" className="max-h-40 mx-auto rounded-md object-cover" />
                ) : (
                  <div className="py-6 text-slate-400">
                    <p className="text-sm">Click to upload soil image</p>
                    <span className="text-xs text-slate-500">Supports JPG, PNG</span>
                  </div>
                )}
              </label>
            </div>

            {/* Telemetry Inputs Grid */}
            <div className="grid grid-cols-2 gap-3 text-xs">
              {Object.keys(telemetry).map((key) => (
                <div key={key} className="space-y-1">
                  <label className="text-slate-400">{key.replace('_', ' ')}</label>
                  <input
                    type={key === 'Land_Type' ? 'text' : 'number'}
                    step="any"
                    value={(telemetry as any)[key]}
                    onChange={(e) =>
                      setTelemetry({
                        ...telemetry,
                        [key]: key === 'Land_Type' ? e.target.value : parseFloat(e.target.value) || 0,
                      })
                    }
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2 py-1 text-slate-200 focus:outline-none focus:border-emerald-500"
                  />
                </div>
              ))}
            </div>

            {error && <div className="text-rose-400 text-xs">{error}</div>}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-medium py-2.5 rounded-lg transition flex items-center justify-center gap-2 cursor-pointer"
            >
              {loading ? <Loader2 className="h-5 w-5 animate-spin" /> : 'Run Afforestation Analysis'}
            </button>
          </form>

          {/* Output Dashboard Results (7 cols) */}
          <div className="lg:col-span-7 space-y-6">
            <h2 className="text-xl font-semibold text-emerald-400">AI Intelligence & Advisory Dashboard</h2>
            {result ? (
              <div className="space-y-6">
                
                {/* Core Metric Cards */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  
                  <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-1">
                    <Sprout className="h-6 w-6 text-amber-400" />
                    <span className="text-xs text-slate-400">Predicted Soil Type</span>
                    <p className="text-xl font-bold text-slate-100">{result.predicted_soil_type}</p>
                  </div>

                  <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-1">
                    <TreePine className="h-6 w-6 text-emerald-400" />
                    <span className="text-xs text-slate-400">Primary Species Match</span>
                    <p className="text-xl font-bold text-slate-100">{result.recommended_tree}</p>
                    <span className="text-xs text-slate-500">Maturation: {result.maturation_years} Years</span>
                  </div>

                  <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-1">
                    <ShieldCheck className="h-6 w-6 text-blue-400" />
                    <span className="text-xs text-slate-400">Survival Probability</span>
                    <p className="text-xl font-bold text-slate-100">{result.survival_probability}%</p>
                  </div>

                  <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-1">
                    <Cloud className="h-6 w-6 text-cyan-400" />
                    <span className="text-xs text-slate-400">Carbon Offset (Tons/Yr)</span>
                    <p className="text-xl font-bold text-slate-100">{result.carbon_offset_tons_per_year}</p>
                  </div>

                </div>

                {/* FEATURE 1: Stress Matrix Badges */}
                <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-3">
                  <h3 className="text-sm font-semibold text-slate-300 flex items-center gap-2">
                    <AlertCircle className="h-4 w-4 text-amber-400" /> Environmental Stress Analysis
                  </h3>
                  <div className="grid grid-cols-3 gap-2 text-xs">
                    <div className="bg-slate-950 p-2.5 rounded border border-slate-800 text-center">
                      <span className="text-slate-400 block text-[10px]">pH Stress</span>
                      <span className="font-semibold text-amber-300">{result.stress_matrix.ph_status}</span>
                    </div>
                    <div className="bg-slate-950 p-2.5 rounded border border-slate-800 text-center">
                      <span className="text-slate-400 block text-[10px]">Thermal Risk</span>
                      <span className="font-semibold text-emerald-300">{result.stress_matrix.thermal_risk}</span>
                    </div>
                    <div className="bg-slate-950 p-2.5 rounded border border-slate-800 text-center">
                      <span className="text-slate-400 block text-[10px]">AQI Impact</span>
                      <span className="font-semibold text-cyan-300">{result.stress_matrix.aqi_impact}</span>
                    </div>
                  </div>
                </div>

                {/* FEATURE 2: Soil Advisory Box */}
                <div className="bg-emerald-950/30 border border-emerald-800/50 p-4 rounded-xl space-y-1">
                  <span className="text-xs font-semibold text-emerald-400 flex items-center gap-1">
                    <Sprout className="h-4 w-4" /> Soil Health Advisory
                  </span>
                  <p className="text-xs text-slate-300">{result.soil_advisory}</p>
                </div>

                {/* FEATURE 3: Biodiversity / Alternative Trees */}
                <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-2">
                  <h3 className="text-sm font-semibold text-slate-300 flex items-center gap-2">
                    <Layers className="h-4 w-4 text-emerald-400" /> Recommended Biodiversity Alternatives
                  </h3>
                  <div className="flex gap-3 text-xs">
                    {result.alternative_species.map((alt, idx) => (
                      <span key={idx} className="bg-slate-950 border border-slate-800 px-3 py-1.5 rounded text-slate-300">
                        {alt}
                      </span>
                    ))}
                  </div>
                </div>

                {/* FEATURE 4: Multi-Scenario ROI Table */}
                <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-3">
                  <h3 className="text-sm font-semibold text-emerald-400 flex items-center gap-2">
                    <TrendingUp className="h-4 w-4" /> Carbon Credit Financial ROI Scenarios
                  </h3>
                  <div className="grid grid-cols-3 gap-2 text-center text-xs">
                    <div className="bg-slate-950 p-3 rounded border border-slate-800">
                      <span className="text-slate-500 block text-[10px]">Conservative ($15/t)</span>
                      <span className="text-slate-200 font-bold text-sm">${result.roi_scenarios.conservative_usd}</span>
                    </div>
                    <div className="bg-emerald-950/40 p-3 rounded border border-emerald-800/80">
                      <span className="text-emerald-400 block text-[10px]">Expected ($20/t)</span>
                      <span className="text-emerald-300 font-bold text-base">${result.roi_scenarios.expected_usd}</span>
                    </div>
                    <div className="bg-slate-950 p-3 rounded border border-slate-800">
                      <span className="text-slate-500 block text-[10px]">Optimistic ($30/t)</span>
                      <span className="text-slate-200 font-bold text-sm">${result.roi_scenarios.optimistic_usd}</span>
                    </div>
                  </div>
                </div>

              </div>
            ) : (
              <div className="bg-slate-900/50 border border-slate-800 border-dashed rounded-xl p-16 text-center text-slate-500">
                Upload image and run analysis to populate multi-scenario ROI, stress matrices, and soil health advisory.
              </div>
            )}
          </div>

        </div>
      </div>
    </main>
  );
}