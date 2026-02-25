import { GraduationCap, Heart, DollarSign, Globe, Users, TrendingUp, CheckCircle2 } from 'lucide-react';

const impacts = [
  {
    icon: GraduationCap,
    title: 'Educational Impact',
    items: ['Improves access to knowledge', 'Supports exam preparation', 'Reduces digital inequality'],
    color: 'teal',
    gradient: 'from-teal/10 to-teal/5',
  },
  {
    icon: Heart,
    title: 'Gender Impact',
    items: ['Promotes STEM participation for girls', 'Encourages female academic excellence', 'Role models & mentorship'],
    color: 'sage',
    gradient: 'from-sage/10 to-sage/5',
  },
  {
    icon: DollarSign,
    title: 'Economic Impact',
    items: ['Low operational cost', 'No expensive devices required', 'Works on basic phones'],
    color: 'teal',
    gradient: 'from-teal/10 to-teal/5',
  },
];

const countries = [
  { name: 'Kenya', flag: '🇰🇪', focus: 'Nairobi, Rural Counties' },
  { name: 'Uganda', flag: '🇺🇬', focus: 'Kampala, Northern Region' },
  { name: 'Tanzania', flag: '🇹🇿', focus: 'Dar es Salaam, Mwanza' },
];

export default function ImpactSection() {
  return (
    <section id="impact" className="py-28 sm:py-32 bg-white relative">
      <div className="max-w-6xl mx-auto px-6 sm:px-8 lg:px-12">
        {/* Section Header */}
        <div className="text-center max-w-2xl mx-auto mb-20">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-teal/8 text-teal rounded-full text-xs font-bold uppercase tracking-widest mb-5 border border-teal/10">
            Impact
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-gray-900 mb-6 leading-tight tracking-tight">
            Transforming <span className="gradient-text">Education Access</span>
            <br />Across East Africa
          </h2>
          <p className="text-gray-400 leading-relaxed text-lg">
            MaktabaAI bridges the digital divide — reaching underserved communities with 
            knowledge through technology they already have.
          </p>
        </div>

        {/* Impact Cards */}
        <div className="grid md:grid-cols-3 gap-6 lg:gap-8 mb-24">
          {impacts.map((impact, idx) => {
            const Icon = impact.icon;
            const isTeal = impact.color === 'teal';
            const iconBg = isTeal ? 'bg-teal/10' : 'bg-sage/10';
            const iconColor = isTeal ? 'text-teal' : 'text-sage';
            const accentColor = isTeal ? 'border-t-teal' : 'border-t-sage';
            const checkColor = isTeal ? 'text-teal' : 'text-sage';

            return (
              <div key={idx} className={`group p-8 rounded-3xl bg-gradient-to-b ${impact.gradient} border border-gray-100 ${accentColor} border-t-4 hover:shadow-xl transition-all duration-300 hover:-translate-y-1`}>
                <div className={`w-14 h-14 ${iconBg} rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  <Icon className={`w-7 h-7 ${iconColor}`} />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-5">{impact.title}</h3>
                <ul className="space-y-3">
                  {impact.items.map((item, i) => (
                    <li key={i} className="flex items-start gap-3 text-sm text-gray-500">
                      <CheckCircle2 className={`w-4 h-4 ${checkColor} mt-0.5 shrink-0`} />
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            );
          })}
        </div>

        {/* Country Coverage */}
        <div className="bg-gradient-to-br from-cream via-cream to-cream-dark/30 rounded-3xl p-10 sm:p-14">
          <div className="flex items-center gap-3 mb-10">
            <div className="w-10 h-10 bg-teal/10 rounded-xl flex items-center justify-center">
              <Globe className="w-5 h-5 text-teal" />
            </div>
            <h3 className="font-heading text-xl font-bold text-gray-900">Country Coverage</h3>
          </div>
          <div className="grid sm:grid-cols-3 gap-6">
            {countries.map((country) => (
              <div key={country.name} className="bg-white p-7 rounded-2xl shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 border border-gray-50">
                <p className="text-4xl mb-3">{country.flag}</p>
                <h4 className="font-bold text-gray-900 text-lg">{country.name}</h4>
                <p className="text-sm text-gray-400 mt-1">{country.focus}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Sustainability */}
        <div className="mt-16 grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {[
            { icon: Users, label: 'Government Partnerships' },
            { icon: Heart, label: 'NGO Educational Grants' },
            { icon: TrendingUp, label: 'Library Subscriptions' },
            { icon: DollarSign, label: 'Sponsored Content' },
          ].map((item, idx) => {
            const Icon = item.icon;
            return (
              <div key={idx} className="flex items-center gap-4 p-5 bg-cream/60 rounded-2xl hover:bg-cream transition-colors group">
                <div className="w-11 h-11 bg-white rounded-xl flex items-center justify-center shrink-0 shadow-sm group-hover:shadow-md transition-shadow">
                  <Icon className="w-5 h-5 text-teal" />
                </div>
                <span className="text-sm font-semibold text-gray-700">{item.label}</span>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
