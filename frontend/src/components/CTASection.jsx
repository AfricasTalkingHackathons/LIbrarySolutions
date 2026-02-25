import { Link } from "react-router-dom";
import { Phone, ArrowRight, Sparkles } from "lucide-react";

export default function CTASection() {
  return (
    <section className="py-28 sm:py-32 bg-gradient-to-br from-teal via-teal-dark to-[#004d4d] relative overflow-hidden">
      {/* Modern decorative blobs */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 left-0 w-72 h-72 bg-white/[0.04] rounded-full blur-3xl" />
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-sage/[0.08] rounded-full blur-3xl" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-white/[0.02] rounded-full blur-3xl" />
        {/* Grid dots */}
        <div
          className="absolute inset-0 opacity-[0.05]"
          style={{
            backgroundImage:
              "radial-gradient(circle, white 1px, transparent 1px)",
            backgroundSize: "30px 30px",
          }}
        />
      </div>

      <div className="relative max-w-4xl mx-auto px-6 sm:px-8 lg:px-12 text-center">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-white/10 text-white/80 rounded-full text-xs font-bold uppercase tracking-widest mb-8 border border-white/10">
          <Sparkles className="w-3.5 h-3.5" />
          Get Started
        </div>

        <h2 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-white mb-8 leading-tight tracking-tight">
          Knowledge Shouldn't
          <br />
          Require Internet
        </h2>
        <p className="text-lg sm:text-xl text-white/60 mb-12 max-w-2xl mx-auto leading-relaxed">
          Join MaktabaAI in bridging the digital divide. Help us bring library
          services to millions of students across East Africa through the
          simplest technology — a phone call.
        </p>

        <div className="flex flex-wrap justify-center gap-5">
          <Link
            to="/demo"
            className="inline-flex items-center gap-2.5 px-8 py-4 bg-white text-teal-dark font-bold rounded-2xl hover:bg-cream hover:shadow-2xl transition-all duration-300 hover:-translate-y-0.5 text-base"
          >
            <Phone className="w-5 h-5" />
            Try the USSD Demo
          </Link>
          <Link
            to="/dashboard"
            className="inline-flex items-center gap-2.5 px-8 py-4 border-2 border-white/20 text-white font-bold rounded-2xl hover:bg-white/10 hover:border-white/40 transition-all duration-300 hover:-translate-y-0.5 text-base"
          >
            View Dashboard
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>

        <p className="mt-10 text-sm text-white/40">
          Dial <strong className="text-white/70">*789*5960#</strong> from any
          phone in Kenya, Uganda, or Tanzania.
        </p>
      </div>
    </section>
  );
}
