import { Link } from "react-router-dom";
import {
  Phone,
  WifiOff,
  ArrowRight,
  BookOpen,
  MessageSquare,
  GraduationCap,
  Zap,
} from "lucide-react";

export default function HeroSection() {
  return (
    <section className="relative min-h-screen flex items-center overflow-hidden bg-gradient-to-b from-cream/60 via-white to-white">
      {/* Rich background decorations */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-60 -right-60 w-[500px] h-[500px] bg-teal/[0.07] rounded-full blur-3xl animate-pulse-soft" />
        <div className="absolute -bottom-60 -left-60 w-[500px] h-[500px] bg-sage/[0.1] rounded-full blur-3xl animate-pulse-soft animate-delay-200" />
        <div className="absolute top-1/3 left-1/2 -translate-x-1/2 w-[700px] h-[700px] bg-gradient-to-br from-teal/[0.04] to-sage/[0.04] rounded-full blur-3xl" />
        {/* Dot grid pattern */}
        <div
          className="absolute inset-0 opacity-[0.03]"
          style={{
            backgroundImage:
              "radial-gradient(circle, #008080 1px, transparent 1px)",
            backgroundSize: "32px 32px",
          }}
        />
      </div>

      <div className="relative max-w-6xl mx-auto px-6 sm:px-8 lg:px-12 pt-32 pb-24">
        <div className="grid lg:grid-cols-2 gap-16 lg:gap-20 items-center">
          {/* Left column */}
          <div className="space-y-10 animate-fade-in-up">
            <div className="inline-flex items-center gap-2.5 px-5 py-2.5 bg-teal/8 text-teal rounded-full text-sm font-semibold border border-teal/15">
              <WifiOff className="w-4 h-4" />
              <span>Works Without Internet</span>
              <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
            </div>

            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-extrabold leading-[1.08] text-gray-900 tracking-tight">
              A Library in
              <br />
              <span className="gradient-text">Every Pocket</span>
            </h1>

            <p className="text-lg sm:text-xl text-gray-500 max-w-xl leading-relaxed">
              MaktabaAI brings digital library services to feature phones across
              East Africa. Search books, get summaries, reserve materials — all
              via{" "}
              <span className="text-gray-800 font-semibold">USSD & SMS</span>.
              No internet required.
            </p>

            <div className="flex flex-wrap gap-4 pt-2">
              <Link
                to="/demo"
                className="inline-flex items-center gap-2.5 px-7 py-3.5 bg-gradient-to-r from-teal to-teal-dark text-white font-semibold rounded-2xl hover:shadow-xl hover:shadow-teal/20 transition-all duration-300 hover:-translate-y-0.5 text-base"
              >
                <Phone className="w-5 h-5" />
                Try USSD Demo
              </Link>
              <a
                href="#features"
                className="inline-flex items-center gap-2.5 px-7 py-3.5 bg-white border-2 border-gray-200 text-gray-700 font-semibold rounded-2xl hover:border-teal/40 hover:text-teal hover:shadow-lg transition-all duration-300 hover:-translate-y-0.5 text-base"
              >
                Learn More
                <ArrowRight className="w-5 h-5" />
              </a>
            </div>

            {/* Stats */}
            <div className="flex gap-10 pt-6">
              {[
                { label: "Countries", value: "3", icon: "🌍" },
                { label: "Target Users", value: "1M+", icon: "👥" },
                { label: "Offline", value: "100%", icon: "📱" },
              ].map((stat) => (
                <div key={stat.label} className="text-center">
                  <p className="text-3xl font-extrabold gradient-text">
                    {stat.value}
                  </p>
                  <p className="text-sm text-gray-400 mt-1 font-medium">
                    {stat.label}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Right column — Phone mockup */}
          <div className="flex justify-center animate-fade-in-up animate-delay-300">
            <div className="relative">
              {/* Glow behind phone */}
              <div className="absolute inset-0 bg-gradient-to-br from-teal/20 to-sage/20 rounded-[3rem] blur-3xl scale-110 opacity-60" />

              {/* Floating icons */}
              <div className="absolute -top-8 -left-10 w-16 h-16 bg-white/90 backdrop-blur-sm rounded-2xl flex items-center justify-center shadow-xl shadow-sage/10 animate-float border border-sage/10">
                <BookOpen className="w-8 h-8 text-sage" />
              </div>
              <div className="absolute -top-3 -right-12 w-14 h-14 bg-white/90 backdrop-blur-sm rounded-2xl flex items-center justify-center shadow-xl shadow-teal/10 animate-float animate-delay-200 border border-teal/10">
                <MessageSquare className="w-7 h-7 text-teal" />
              </div>
              <div className="absolute -bottom-6 -left-8 w-14 h-14 bg-white/90 backdrop-blur-sm rounded-2xl flex items-center justify-center shadow-xl shadow-teal/10 animate-float animate-delay-400 border border-teal/10">
                <GraduationCap className="w-7 h-7 text-teal" />
              </div>
              <div className="absolute bottom-16 -right-10 w-12 h-12 bg-white/90 backdrop-blur-sm rounded-2xl flex items-center justify-center shadow-xl shadow-sage/10 animate-float animate-delay-600 border border-sage/10">
                <Zap className="w-6 h-6 text-sage" />
              </div>

              {/* Phone */}
              <div className="relative ussd-phone w-[300px]">
                <div className="w-20 h-1.5 bg-gray-600/60 rounded-full mx-auto mb-5" />
                <div className="ussd-screen">
                  <p className="font-bold mb-2 text-sm">📚 MaktabaAI</p>
                  <p className="mb-3">Welcome! Choose an option:</p>
                  <p>1. Search Book</p>
                  <p>2. Request Summary</p>
                  <p>3. Reserve Book</p>
                  <p>4. Revision Materials</p>
                  <p>5. Ask Librarian</p>
                  <p>6. Girls STEM Mode</p>
                  <div className="mt-4 pt-2 border-t border-green-800/20">
                    <p className="text-xs opacity-60">
                      Dial *789*5960# to access
                    </p>
                  </div>
                </div>
                <div className="mt-5 flex justify-center">
                  <div className="w-14 h-14 border-2 border-gray-600/40 rounded-full hover:border-gray-400 transition-colors" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom fade into next section */}
      <div className="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-white to-transparent" />
    </section>
  );
}
