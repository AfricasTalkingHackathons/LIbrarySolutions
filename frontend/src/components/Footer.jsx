import { Link } from "react-router-dom";
import {
  BookOpen,
  Mail,
  Phone,
  MapPin,
  Github,
  Twitter,
  Linkedin,
} from "lucide-react";

export default function Footer() {
  return (
    <footer className="bg-midnight text-gray-400">
      <div className="max-w-6xl mx-auto px-6 sm:px-8 lg:px-12 py-20">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12">
          {/* Brand */}
          <div className="space-y-5">
            <Link to="/" className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-teal to-teal-dark rounded-xl flex items-center justify-center">
                <BookOpen className="w-5 h-5 text-white" />
              </div>
              <span className="font-heading text-xl font-bold text-white">
                Maktaba<span className="text-teal-light">AI</span>
              </span>
            </Link>
            <p className="text-sm leading-relaxed text-gray-500">
              Bridging Africa's digital divide through USSD and SMS-based
              library access. Knowledge doesn't require internet.
            </p>
            <div className="flex gap-3">
              {[Twitter, Github, Linkedin].map((Icon, idx) => (
                <a
                  key={idx}
                  href="#"
                  className="w-10 h-10 bg-white/5 rounded-xl flex items-center justify-center hover:bg-teal/20 hover:text-teal transition-all duration-200"
                >
                  <Icon className="w-4 h-4" />
                </a>
              ))}
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-white font-heading font-semibold mb-5 text-sm">
              Quick Links
            </h4>
            <ul className="space-y-3">
              {[
                "Features",
                "How It Works",
                "Impact",
                "USSD Demo",
                "Dashboard",
              ].map((item) => (
                <li key={item}>
                  <Link
                    to={
                      item === "Dashboard"
                        ? "/dashboard"
                        : item === "USSD Demo"
                          ? "/demo"
                          : `/#${item.toLowerCase().replace(/ /g, "-")}`
                    }
                    className="text-sm text-gray-500 hover:text-teal-light transition-colors duration-200"
                  >
                    {item}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Coverage */}
          <div>
            <h4 className="text-white font-heading font-semibold mb-5 text-sm">
              Coverage
            </h4>
            <ul className="space-y-3 text-sm">
              {["Kenya", "Uganda", "Tanzania"].map((country) => (
                <li
                  key={country}
                  className="flex items-center gap-3 text-gray-500"
                >
                  <MapPin className="w-4 h-4 text-teal/60" />
                  {country}
                </li>
              ))}
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="text-white font-heading font-semibold mb-5 text-sm">
              Contact
            </h4>
            <ul className="space-y-4 text-sm">
              <li className="flex items-center gap-3 text-gray-500">
                <div className="w-8 h-8 bg-white/5 rounded-lg flex items-center justify-center shrink-0">
                  <Phone className="w-4 h-4 text-teal/60" />
                </div>
                <span>Dial *789*5960#</span>
              </li>
              <li className="flex items-center gap-3 text-gray-500">
                <div className="w-8 h-8 bg-white/5 rounded-lg flex items-center justify-center shrink-0">
                  <Mail className="w-4 h-4 text-teal/60" />
                </div>
                <span>hello@maktaba-ai.org</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-16 pt-8 border-t border-white/5 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-gray-600">
            &copy; {new Date().getFullYear()} MaktabaAI. All rights reserved.
          </p>
          <p className="text-xs text-gray-600">
            Built with purpose for Africa's learners.
          </p>
        </div>
      </div>
    </footer>
  );
}
