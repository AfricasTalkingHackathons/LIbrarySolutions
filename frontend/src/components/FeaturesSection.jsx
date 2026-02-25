import { Search, FileText, CalendarCheck, BookMarked, MessageCircle, Sparkles } from 'lucide-react';

const features = [
  {
    icon: Search,
    title: 'Book Search via USSD',
    description: 'Enter keywords to search. Get matching titles, availability status, and reserve instantly — all through a simple USSD menu.',
    color: 'teal',
  },
  {
    icon: FileText,
    title: 'SMS Book Summaries',
    description: 'Receive concise key insights and curriculum-aligned academic summaries directly via SMS. Perfect for exam preparation.',
    color: 'sage',
  },
  {
    icon: CalendarCheck,
    title: 'Book Reservation',
    description: 'Reserve available books remotely. Receive SMS confirmation and reminders before the due date. No visit needed.',
    color: 'teal',
  },
  {
    icon: BookMarked,
    title: 'Revision & Academic Support',
    description: 'Select your subject and topic, then receive summarized revision notes via SMS. Curriculum-aligned content for students.',
    color: 'sage',
  },
  {
    icon: MessageCircle,
    title: 'Ask Librarian (AI)',
    description: 'Send academic questions via SMS and receive simplified AI-powered explanations. Like having a tutor on your phone.',
    color: 'teal',
  },
  {
    icon: Sparkles,
    title: 'Girls STEM Mode',
    description: 'Dedicated content for young women: career guidance, STEM motivation, scholarships, and inspiring role model profiles.',
    color: 'sage',
  },
];

export default function FeaturesSection() {
  return (
    <section id="features" className="py-28 sm:py-32 bg-white relative">
      <div className="max-w-6xl mx-auto px-6 sm:px-8 lg:px-12">
        {/* Section Header */}
        <div className="text-center max-w-2xl mx-auto mb-20">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-teal/8 text-teal rounded-full text-xs font-bold uppercase tracking-widest mb-5 border border-teal/10">
            <Sparkles className="w-3.5 h-3.5" />
            Features
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-gray-900 mb-6 leading-tight tracking-tight">
            Everything a Library Offers,
            <br />
            <span className="gradient-text">Right on Your Phone</span>
          </h2>
          <p className="text-gray-400 leading-relaxed text-lg">
            MaktabaAI delivers full digital library services through USSD and SMS — 
            no internet, no smartphone, no barriers.
          </p>
        </div>

        {/* Feature Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8">
          {features.map((feature, idx) => {
            const Icon = feature.icon;
            const isTeal = feature.color === 'teal';
            const bgColor = isTeal ? 'bg-teal/8' : 'bg-sage/8';
            const iconColor = isTeal ? 'text-teal' : 'text-sage';
            const gradientBorder = isTeal
              ? 'hover:shadow-teal/8'
              : 'hover:shadow-sage/8';

            return (
              <div
                key={idx}
                className={`group relative p-8 rounded-3xl border border-gray-100 bg-white transition-all duration-300 hover:shadow-2xl ${gradientBorder} hover:-translate-y-1.5 hover:border-transparent`}
              >
                {/* Gradient border on hover */}
                <div className="absolute inset-0 rounded-3xl bg-gradient-to-br from-teal/10 to-sage/10 opacity-0 group-hover:opacity-100 transition-opacity -z-10 scale-[1.02]" />
                
                <div className={`w-14 h-14 ${bgColor} rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  <Icon className={`w-7 h-7 ${iconColor}`} />
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-3">{feature.title}</h3>
                <p className="text-sm text-gray-400 leading-relaxed">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
