import { Phone, Radio, Server, MessageSquare, ArrowRight } from "lucide-react";

const steps = [
  {
    icon: Phone,
    step: "01",
    title: "Dial *789*5960#",
    description:
      "Pick up any phone — feature phone or smartphone — and dial the USSD short code to start.",
    accent: "from-teal to-teal-dark",
  },
  {
    icon: Radio,
    step: "02",
    title: "Navigate the Menu",
    description:
      "Browse an interactive menu: search books, request summaries, reserve materials, or ask questions.",
    accent: "from-sage to-sage-dark",
  },
  {
    icon: Server,
    step: "03",
    title: "AI Processes Request",
    description:
      "Your request reaches our backend via Africa's Talking API. AI generates relevant, curriculum-aligned content.",
    accent: "from-teal to-teal-dark",
  },
  {
    icon: MessageSquare,
    step: "04",
    title: "Get SMS Response",
    description:
      "Receive book summaries, revision notes, reservation confirmations, or answers — all via SMS.",
    accent: "from-sage to-sage-dark",
  },
];

export default function HowItWorksSection() {
  return (
    <section
      id="how-it-works"
      className="py-28 sm:py-32 bg-gradient-to-b from-cream/50 via-cream to-cream/50 relative"
    >
      {/* Subtle background pattern */}
      <div
        className="absolute inset-0 opacity-[0.02] pointer-events-none"
        style={{
          backgroundImage:
            "radial-gradient(circle, #008080 1px, transparent 1px)",
          backgroundSize: "40px 40px",
        }}
      />

      <div className="relative max-w-6xl mx-auto px-6 sm:px-8 lg:px-12">
        {/* Section Header */}
        <div className="text-center max-w-2xl mx-auto mb-20">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-sage/10 text-sage-dark rounded-full text-xs font-bold uppercase tracking-widest mb-5 border border-sage/15">
            How It Works
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-gray-900 mb-6 leading-tight tracking-tight">
            Simple. Accessible. <span className="gradient-text">Powerful.</span>
          </h2>
          <p className="text-gray-400 leading-relaxed text-lg">
            Four simple steps connect any user to a world of knowledge — using
            only a basic cellphone and the cellular network.
          </p>
        </div>

        {/* Steps */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 lg:gap-6">
          {steps.map((item, idx) => {
            const Icon = item.icon;
            return (
              <div key={idx} className="relative text-center group">
                {/* Connector arrow */}
                {idx < steps.length - 1 && (
                  <div className="hidden lg:flex absolute top-14 left-[65%] w-[70%] items-center justify-center">
                    <div className="w-full h-[2px] bg-gradient-to-r from-teal/20 to-sage/20 rounded-full" />
                    <ArrowRight className="w-4 h-4 text-teal/30 -ml-1 shrink-0" />
                  </div>
                )}

                <div className="relative inline-flex items-center justify-center w-28 h-28 bg-white rounded-3xl shadow-lg shadow-black/[0.04] group-hover:shadow-xl group-hover:shadow-teal/10 transition-all duration-300 mb-7 group-hover:-translate-y-1">
                  <Icon className="w-11 h-11 text-teal" />
                  <span
                    className={`absolute -top-3 -right-3 w-9 h-9 bg-gradient-to-br ${item.accent} text-white text-xs font-bold rounded-xl flex items-center justify-center shadow-lg`}
                  >
                    {item.step}
                  </span>
                </div>

                <h3 className="text-lg font-bold text-gray-900 mb-3">
                  {item.title}
                </h3>
                <p className="text-sm text-gray-400 leading-relaxed max-w-[240px] mx-auto">
                  {item.description}
                </p>
              </div>
            );
          })}
        </div>

        {/* Architecture diagram */}
        <div className="mt-24 p-10 bg-white rounded-3xl shadow-lg shadow-black/[0.03] border border-gray-100">
          <h3 className="text-center font-heading font-bold text-gray-900 mb-10 text-lg">
            System Architecture
          </h3>
          <div className="flex flex-wrap justify-center items-center gap-3 text-sm">
            {[
              {
                label: "Feature Phone",
                color:
                  "bg-gradient-to-r from-teal/10 to-teal/5 text-teal border border-teal/10",
              },
              { label: "→" },
              {
                label: "USSD Request",
                color:
                  "bg-gradient-to-r from-sage/10 to-sage/5 text-sage-dark border border-sage/10",
              },
              { label: "→" },
              {
                label: "Africa's Talking API",
                color:
                  "bg-gradient-to-r from-teal/10 to-teal/5 text-teal border border-teal/10",
              },
              { label: "→" },
              {
                label: "Backend Server",
                color:
                  "bg-gradient-to-r from-sage/10 to-sage/5 text-sage-dark border border-sage/10",
              },
              { label: "→" },
              {
                label: "Database",
                color:
                  "bg-gradient-to-r from-teal/10 to-teal/5 text-teal border border-teal/10",
              },
              { label: "→" },
              {
                label: "SMS Response",
                color:
                  "bg-gradient-to-r from-sage/10 to-sage/5 text-sage-dark border border-sage/10",
              },
              { label: "→" },
              {
                label: "User",
                color:
                  "bg-gradient-to-r from-teal/10 to-teal/5 text-teal border border-teal/10",
              },
            ].map((item, idx) =>
              item.color ? (
                <span
                  key={idx}
                  className={`px-5 py-2.5 rounded-xl font-semibold text-xs ${item.color}`}
                >
                  {item.label}
                </span>
              ) : (
                <span key={idx} className="text-gray-300 font-bold text-lg">
                  →
                </span>
              ),
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
