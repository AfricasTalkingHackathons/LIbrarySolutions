import { useState } from "react";
import { Phone, RotateCcw, Send } from "lucide-react";
import { mockBooks } from "../data/mockData";

const MENUS = {
  main: {
    title: "📚 MaktabaAI",
    text: "Welcome! Choose an option:",
    options: [
      { key: "1", label: "Search Book", next: "search_prompt" },
      { key: "2", label: "Request Summary", next: "summary_prompt" },
      { key: "3", label: "Reserve Book", next: "reserve_prompt" },
      { key: "4", label: "Revision Materials", next: "revision_subject" },
      { key: "5", label: "Ask Librarian", next: "ask_prompt" },
      { key: "6", label: "Girls STEM Mode", next: "stem_menu" },
    ],
  },
  search_prompt: {
    title: "🔍 Search Book",
    text: "Enter a keyword to search:",
    input: true,
    handler: "search",
  },
  summary_prompt: {
    title: "📖 Request Summary",
    text: "Enter the book title:",
    input: true,
    handler: "summary",
  },
  reserve_prompt: {
    title: "📅 Reserve Book",
    text: "Enter the book title to reserve:",
    input: true,
    handler: "reserve",
  },
  revision_subject: {
    title: "📝 Revision Materials",
    text: "Select a subject:",
    options: [
      { key: "1", label: "Mathematics", next: "revision_topic_math" },
      { key: "2", label: "Physics", next: "revision_topic_physics" },
      { key: "3", label: "Biology", next: "revision_topic_bio" },
      { key: "4", label: "History", next: "revision_topic_history" },
    ],
  },
  revision_topic_math: {
    title: "📐 Mathematics",
    text: "Select a topic:",
    options: [
      { key: "1", label: "Algebra", next: "revision_result_algebra" },
      { key: "2", label: "Geometry", next: "revision_result_geometry" },
      { key: "3", label: "Trigonometry", next: "revision_result_trig" },
    ],
  },
  revision_topic_physics: {
    title: "⚡ Physics",
    text: "Select a topic:",
    options: [
      { key: "1", label: "Newton's Laws", next: "revision_result_newton" },
      { key: "2", label: "Waves", next: "revision_result_waves" },
    ],
  },
  revision_topic_bio: {
    title: "🧬 Biology",
    text: "Select a topic:",
    options: [
      { key: "1", label: "Cell Biology", next: "revision_result_cell" },
      { key: "2", label: "Ecology", next: "revision_result_ecology" },
    ],
  },
  revision_topic_history: {
    title: "📜 History",
    text: "Select a topic:",
    options: [
      { key: "1", label: "Pre-colonial EA", next: "revision_result_precol" },
      { key: "2", label: "Independence", next: "revision_result_indep" },
    ],
  },
  revision_result_algebra: {
    title: "📐 Algebra Notes",
    text: "KEY CONCEPTS:\n• Variables represent unknown values\n• Solve by isolating the variable\n• Balance both sides of equation\n• Example: 2x + 3 = 7 → x = 2\n\n📱 SMS sent with full notes!",
    end: true,
  },
  revision_result_geometry: {
    title: "📐 Geometry Notes",
    text: "KEY CONCEPTS:\n• Area of triangle = ½ × base × height\n• Pythagoras: a² + b² = c²\n• Circle area = πr²\n\n📱 SMS sent with full notes!",
    end: true,
  },
  revision_result_trig: {
    title: "📐 Trigonometry Notes",
    text: "KEY CONCEPTS:\n• SOH-CAH-TOA\n• sin θ = opposite/hypotenuse\n• cos θ = adjacent/hypotenuse\n• tan θ = opposite/adjacent\n\n📱 SMS sent with full notes!",
    end: true,
  },
  revision_result_newton: {
    title: "⚡ Newton's Laws",
    text: "KEY CONCEPTS:\n1st Law: Object at rest stays at rest\n2nd Law: F = ma\n3rd Law: Every action has an equal opposite reaction\n\n📱 SMS sent with full notes!",
    end: true,
  },
  revision_result_waves: {
    title: "⚡ Waves Notes",
    text: "KEY CONCEPTS:\n• Waves transfer energy not matter\n• Speed = frequency × wavelength\n• Types: transverse, longitudinal\n\n📱 SMS sent with full notes!",
    end: true,
  },
  revision_result_cell: {
    title: "🧬 Cell Biology",
    text: "KEY CONCEPTS:\n• Cell is basic unit of life\n• Organelles: nucleus, mitochondria, ribosomes\n• Plant cells have cell walls\n\n📱 SMS sent with full notes!",
    end: true,
  },
  revision_result_ecology: {
    title: "🧬 Ecology Notes",
    text: "KEY CONCEPTS:\n• Ecosystem = biotic + abiotic\n• Food chains show energy flow\n• Biodiversity maintains balance\n\n📱 SMS sent with full notes!",
    end: true,
  },
  revision_result_precol: {
    title: "📜 Pre-colonial EA",
    text: "KEY POINTS:\n• Diverse kingdoms and chiefdoms\n• Swahili coast trade networks\n• Bantu migration shaped region\n\n📱 SMS sent with full notes!",
    end: true,
  },
  revision_result_indep: {
    title: "📜 Independence",
    text: "KEY POINTS:\n• Kenya: 1963 (Kenyatta)\n• Uganda: 1962 (Obote)\n• Tanzania: 1961 (Nyerere)\n• Pan-African movements drove change\n\n📱 SMS sent with full notes!",
    end: true,
  },
  ask_prompt: {
    title: "🤖 Ask Librarian",
    text: "Type your academic question:",
    input: true,
    handler: "ask",
  },
  stem_menu: {
    title: "👩‍🔬 Girls STEM Mode",
    text: "Empowering young women in STEM:",
    options: [
      { key: "1", label: "Role Models", next: "stem_rolemodels" },
      { key: "2", label: "Career Guidance", next: "stem_careers" },
      { key: "3", label: "Scholarships", next: "stem_scholarships" },
    ],
  },
  stem_rolemodels: {
    title: "🌟 STEM Role Models",
    text: "🇰🇪 Wangari Maathai\nNobel Peace Prize, environmental activist\n\n💻 Grace Hopper\nComputer science pioneer, invented compiler\n\n🔬 Marie Curie\nFirst woman Nobel Prize winner (Physics & Chemistry)\n\nYou can be the next!",
    end: true,
  },
  stem_careers: {
    title: "🚀 Career Guidance",
    text: "STEM Careers:\n• Software Engineering\n• Medicine & Health\n• Environmental Science\n• Data Science & AI\n• Agricultural Technology\n\n📱 SMS sent with full guide!",
    end: true,
  },
  stem_scholarships: {
    title: "🎓 Scholarships",
    text: "Opportunities:\n• Mastercard Foundation Scholars\n• DAAD East Africa\n• Equity Wings to Fly\n• STEM Girls Africa Fund\n\n📱 SMS sent with details!",
    end: true,
  },
};

export default function USSDDemo() {
  const [menuStack, setMenuStack] = useState(["main"]);
  const [input, setInput] = useState("");
  const [dynamicScreen, setDynamicScreen] = useState(null);

  const currentMenuKey = menuStack[menuStack.length - 1];
  const currentMenu = MENUS[currentMenuKey];

  const handleSelect = (option) => {
    if (option.next) {
      setMenuStack([...menuStack, option.next]);
      setDynamicScreen(null);
    }
  };

  const handleInput = () => {
    if (!input.trim()) return;
    const menu = MENUS[currentMenuKey];

    if (menu.handler === "search") {
      const results = mockBooks.filter(
        (b) =>
          b.title.toLowerCase().includes(input.toLowerCase()) ||
          b.author.toLowerCase().includes(input.toLowerCase()) ||
          b.category.toLowerCase().includes(input.toLowerCase()),
      );
      if (results.length > 0) {
        setDynamicScreen({
          title: "🔍 Search Results",
          text: results
            .slice(0, 3)
            .map(
              (b) =>
                `• ${b.title}\n  by ${b.author}\n  ${b.available ? "✅ Available" : "❌ Checked Out"}`,
            )
            .join("\n\n"),
          end: true,
        });
      } else {
        setDynamicScreen({
          title: "🔍 Search Results",
          text: `No books found for "${input}".\nTry different keywords.`,
          end: true,
        });
      }
    } else if (menu.handler === "summary") {
      const book = mockBooks.find((b) =>
        b.title.toLowerCase().includes(input.toLowerCase()),
      );
      if (book) {
        setDynamicScreen({
          title: "📖 Book Summary",
          text: `${book.title}\nby ${book.author}\n\n${book.summary}\n\n📱 Full summary sent via SMS!`,
          end: true,
        });
      } else {
        setDynamicScreen({
          title: "📖 Book Summary",
          text: `Book "${input}" not found.\nPlease check the title.`,
          end: true,
        });
      }
    } else if (menu.handler === "reserve") {
      const book = mockBooks.find((b) =>
        b.title.toLowerCase().includes(input.toLowerCase()),
      );
      if (book && book.available) {
        setDynamicScreen({
          title: "📅 Reservation Confirmed",
          text: `✅ Reserved: ${book.title}\nDue: 2 weeks from today\n\n📱 Confirmation SMS sent!\nYou'll receive a reminder 2 days before due date.`,
          end: true,
        });
      } else if (book) {
        setDynamicScreen({
          title: "📅 Reservation",
          text: `❌ "${book.title}" is currently checked out.\nTry again later.`,
          end: true,
        });
      } else {
        setDynamicScreen({
          title: "📅 Reservation",
          text: `Book "${input}" not found.`,
          end: true,
        });
      }
    } else if (menu.handler === "ask") {
      setDynamicScreen({
        title: "🤖 AI Answer",
        text: `Q: "${input}"\n\nOur AI librarian is processing your question...\n\n📱 Answer will be sent via SMS shortly!\n\n(In production, this connects to OpenAI API)`,
        end: true,
      });
    }

    setInput("");
  };

  const displayMenu = dynamicScreen || currentMenu;

  const handleReset = () => {
    setMenuStack(["main"]);
    setInput("");
    setDynamicScreen(null);
  };

  const handleBack = () => {
    if (menuStack.length > 1) {
      setMenuStack(menuStack.slice(0, -1));
      setDynamicScreen(null);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-cream via-white to-cream pt-32 pb-24">
      <div className="max-w-6xl mx-auto px-6 sm:px-8 lg:px-12">
        <div className="text-center mb-16">
          <span className="inline-block px-4 py-1.5 bg-teal/10 text-teal text-sm font-semibold rounded-full mb-4 tracking-wide">
            Interactive Demo
          </span>
          <h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900 font-heading tracking-tight mb-5">
            Try the <span className="gradient-text">USSD Experience</span>
          </h1>
          <p className="text-gray-500 max-w-lg mx-auto text-lg leading-relaxed">
            Experience how MaktabaAI works on a feature phone. Navigate the
            menu, search books, and explore all features — right here in your
            browser.
          </p>
        </div>

        <div className="flex flex-col lg:flex-row items-start justify-center gap-12">
          {/* Phone simulator */}
          <div className="mx-auto">
            <div className="ussd-phone w-80">
              {/* Earpiece */}
              <div className="w-16 h-1 bg-gray-600 rounded-full mx-auto mb-4" />

              {/* Screen */}
              <div className="ussd-screen min-h-[320px] flex flex-col">
                <p className="font-bold text-sm mb-1">{displayMenu.title}</p>
                <div className="border-b border-green-800/20 mb-2 pb-1" />

                <div className="flex-1 whitespace-pre-wrap text-xs leading-relaxed">
                  <p className="mb-2">{displayMenu.text}</p>
                  {displayMenu.options && (
                    <div className="space-y-0.5">
                      {displayMenu.options.map((opt) => (
                        <p key={opt.key}>
                          {opt.key}. {opt.label}
                        </p>
                      ))}
                    </div>
                  )}
                </div>

                {displayMenu.end && (
                  <div className="border-t border-green-800/20 mt-2 pt-2 text-xs opacity-70">
                    Press any key to return to menu
                  </div>
                )}
              </div>

              {/* Input area */}
              <div className="mt-3 space-y-2">
                {currentMenu?.input && !dynamicScreen ? (
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      onKeyDown={(e) => e.key === "Enter" && handleInput()}
                      placeholder="Type here..."
                      className="flex-1 px-3 py-2 bg-gray-700 text-white text-sm rounded-lg border border-gray-600 focus:outline-none focus:border-teal placeholder-gray-400"
                    />
                    <button
                      onClick={handleInput}
                      className="px-3 py-2 bg-teal text-white rounded-lg hover:bg-teal-dark transition-colors"
                    >
                      <Send className="w-4 h-4" />
                    </button>
                  </div>
                ) : displayMenu.options ? (
                  <div className="grid grid-cols-3 gap-1.5">
                    {displayMenu.options.map((opt) => (
                      <button
                        key={opt.key}
                        onClick={() => handleSelect(opt)}
                        className="px-3 py-2 bg-gray-700 text-white text-sm font-medium rounded-lg hover:bg-gray-600 active:bg-teal transition-colors"
                      >
                        {opt.key}
                      </button>
                    ))}
                  </div>
                ) : (
                  <button
                    onClick={handleReset}
                    className="w-full px-3 py-2 bg-teal text-white text-sm font-medium rounded-lg hover:bg-teal-dark transition-colors"
                  >
                    Back to Main Menu
                  </button>
                )}

                <div className="flex gap-2">
                  {menuStack.length > 1 && (
                    <button
                      onClick={handleBack}
                      className="flex-1 px-3 py-2 bg-gray-800 text-gray-300 text-sm rounded-lg hover:bg-gray-700 transition-colors"
                    >
                      ← Back
                    </button>
                  )}
                  <button
                    onClick={handleReset}
                    className="flex-1 px-3 py-2 bg-gray-800 text-gray-300 text-sm rounded-lg hover:bg-gray-700 transition-colors flex items-center justify-center gap-1"
                  >
                    <RotateCcw className="w-3 h-3" />
                    Reset
                  </button>
                </div>
              </div>

              {/* Home button */}
              <div className="mt-4 flex justify-center">
                <div
                  className="w-12 h-12 border-2 border-gray-600 rounded-full cursor-pointer hover:border-gray-400 transition-colors"
                  onClick={handleReset}
                />
              </div>
            </div>

            <p className="text-center text-xs text-gray-400 mt-4">
              <Phone className="w-3 h-3 inline mr-1" />
              Simulates dialing *789*5960#
            </p>
          </div>

          {/* Instructions panel */}
          <div className="flex-1 max-w-md space-y-6">
            <div className="bg-white rounded-3xl border border-gray-100 p-7 shadow-sm">
              <h3 className="font-heading font-bold text-gray-900 mb-5 text-lg">
                How to Use
              </h3>
              <ol className="space-y-3 text-sm text-gray-600">
                <li className="flex gap-3">
                  <span className="w-6 h-6 bg-teal/10 text-teal rounded-full flex items-center justify-center text-xs font-bold shrink-0">
                    1
                  </span>
                  Click a numbered button to select a menu option
                </li>
                <li className="flex gap-3">
                  <span className="w-6 h-6 bg-teal/10 text-teal rounded-full flex items-center justify-center text-xs font-bold shrink-0">
                    2
                  </span>
                  When prompted, type your query in the input field
                </li>
                <li className="flex gap-3">
                  <span className="w-6 h-6 bg-teal/10 text-teal rounded-full flex items-center justify-center text-xs font-bold shrink-0">
                    3
                  </span>
                  Press Send or Enter to submit your input
                </li>
                <li className="flex gap-3">
                  <span className="w-6 h-6 bg-teal/10 text-teal rounded-full flex items-center justify-center text-xs font-bold shrink-0">
                    4
                  </span>
                  Use Back or Reset to navigate
                </li>
              </ol>
            </div>

            <div className="bg-white rounded-3xl border border-gray-100 p-7 shadow-sm">
              <h3 className="font-heading font-bold text-gray-900 mb-5 text-lg">
                Try These Searches
              </h3>
              <div className="space-y-2">
                {[
                  "Physics",
                  "Chinua Achebe",
                  "Biology",
                  "Things Fall Apart",
                  "Computer",
                ].map((q) => (
                  <span
                    key={q}
                    className="inline-block px-4 py-2 bg-cream text-sage-dark text-sm rounded-xl mr-2 mb-2 cursor-default font-medium hover:bg-teal/10 hover:text-teal transition-colors"
                  >
                    "{q}"
                  </span>
                ))}
              </div>
            </div>

            <div className="bg-teal/5 rounded-3xl border border-teal/10 p-7">
              <h3 className="font-heading font-bold text-teal-dark mb-3 text-lg">
                On a Real Phone
              </h3>
              <p className="text-sm text-gray-600 leading-relaxed">
                In production, users simply dial <strong>*789*5960#</strong>{" "}
                from any phone. No app download, no internet, no smartphone
                needed. The experience is powered by Africa's Talking USSD & SMS
                APIs.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
