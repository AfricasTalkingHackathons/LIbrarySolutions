# MaktabaAI Frontend

A modern, responsive frontend for MaktabaAI - USSD & SMS-Based Digital Library Access Platform.

## 🚀 Features

- **Modern UI/UX Design**: Clean, contemporary interface with Tailwind CSS
- **USSD Simulator**: Interactive testing environment for USSD functionality
- **Book Management**: Complete library inventory management system
- **User Management**: Comprehensive user administration dashboard
- **Reservation System**: Track and manage book reservations
- **Analytics Dashboard**: Real-time usage metrics and insights
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Interactive Components**: Smooth animations and transitions with Framer Motion

## 🛠 Technology Stack

- **React 18**: Modern React with hooks and functional components
- **React Router**: Client-side routing
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Animation library
- **Lucide React**: Modern icon library
- **Recharts**: Data visualization and charts
- **Axios**: HTTP client for API integration

## 📦 Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd maktaba-connect-frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm start
```

The application will be available at `http://localhost:3000`

## 🏗 Project Structure

```
src/
├── components/
│   └── Navbar.js          # Navigation component
├── pages/
│   ├── Dashboard.js       # Main dashboard
│   ├── USSDSimulator.js   # USSD testing interface
│   ├── BookManagement.js  # Book inventory management
│   ├── UserManagement.js  # User administration
│   ├── Reservations.js    # Reservation tracking
│   └── Analytics.js       # Analytics dashboard
├── App.js                 # Main application component
├── index.js              # Application entry point
└── index.css             # Global styles
```

## 🎯 Key Features

### Dashboard

- Real-time statistics and metrics
- Recent activity feed
- Quick action buttons
- Platform overview

### USSD Simulator

- Interactive phone interface
- Real-time session testing
- Multiple test scenarios
- Session history tracking

### Book Management

- Complete CRUD operations
- Advanced search and filtering
- Category management
- Availability tracking

### User Management

- User registration and profiles
- Activity tracking
- Location-based analytics
- Communication tools

### Reservations

- Real-time reservation tracking
- Overdue management
- Automated reminders
- Return processing

### Analytics

- Usage trends and charts
- Performance metrics
- User engagement data
- Export capabilities

## 🎨 Design System

The application uses a modern design system with:

- **Primary Colors**: Blue palette for main actions
- **Secondary Colors**: Green for success states
- **Accent Colors**: Orange for highlights
- **Typography**: Inter font family for readability
- **Spacing**: Consistent 8px grid system
- **Animations**: Smooth transitions and micro-interactions

## 🔧 Configuration

### Tailwind CSS

Custom configuration in `tailwind.config.js` with:

- Extended color palette
- Custom animations
- Responsive breakpoints
- Component utilities

### Build Process

- React Scripts for development and building
- Optimized production builds
- Code splitting and lazy loading
- Asset optimization

## 📱 Responsive Design

The application is fully responsive with:

- Mobile-first approach
- Adaptive layouts
- Touch-friendly interfaces
- Optimized performance

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

### Environment Variables

Create a `.env` file for environment-specific configurations:

```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_USSD_SHORTCODE=*789*5960#
```

## 🔗 Backend Integration

The frontend is designed to integrate with a backend API supporting:

- RESTful endpoints
- Real-time updates via WebSockets
- Authentication and authorization
- File uploads and downloads

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For support and questions, please contact the development team.

---

**MaktabaAI** - Bridging the digital divide through innovative library access solutions.
