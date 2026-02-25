export const mockBooks = [
  { id: 1, title: 'Things Fall Apart', author: 'Chinua Achebe', category: 'Literature', available: true, summary: 'A classic novel exploring the clash between traditional Igbo culture and colonial forces in Nigeria.' },
  { id: 2, title: 'Weep Not, Child', author: 'Ngũgĩ wa Thiong\'o', category: 'Literature', available: true, summary: 'The first major novel in English by an East African, centered on the Mau Mau uprising.' },
  { id: 3, title: 'The River Between', author: 'Ngũgĩ wa Thiong\'o', category: 'Literature', available: false, summary: 'A story of two ridges divided by culture, faith, and a river — and the young man who tries to unite them.' },
  { id: 4, title: 'Born a Crime', author: 'Trevor Noah', category: 'Biography', available: true, summary: 'Trevor Noah\'s memoir of growing up mixed-race in South Africa during apartheid.' },
  { id: 5, title: 'Physics for East Africa', author: 'K. Nderitu', category: 'Science', available: true, summary: 'Comprehensive physics textbook aligned with the East African curriculum covering mechanics, waves, and electricity.' },
  { id: 6, title: 'Introduction to Algebra', author: 'M. Odhiambo', category: 'Mathematics', available: false, summary: 'Foundational algebra concepts for secondary school students with worked examples.' },
  { id: 7, title: 'Biology Form 3', author: 'KICD', category: 'Science', available: true, summary: 'Biology textbook covering ecology, genetics, and human physiology for Form 3 students.' },
  { id: 8, title: 'History of East Africa', author: 'B. Ogot', category: 'History', available: true, summary: 'A comprehensive history spanning pre-colonial, colonial, and post-independence East Africa.' },
  { id: 9, title: 'Kiswahili Masomo', author: 'J. Wamitila', category: 'Language', available: true, summary: 'Kiswahili language and literature for secondary school students.' },
  { id: 10, title: 'Computer Studies Basics', author: 'P. Kimani', category: 'Technology', available: false, summary: 'Introduction to computer science, programming basics, and digital literacy.' },
];

export const mockUsers = [
  { id: 1, phone_number: '+254712345678', name: 'Amina Wanjiku', county: 'Kiambu', created_at: '2025-09-15' },
  { id: 2, phone_number: '+254723456789', name: 'Brian Ochieng', county: 'Kisumu', created_at: '2025-10-02' },
  { id: 3, phone_number: '+256781234567', name: 'Grace Nakato', county: 'Kampala', created_at: '2025-10-18' },
  { id: 4, phone_number: '+255712345678', name: 'Hassan Juma', county: 'Dar es Salaam', created_at: '2025-11-01' },
  { id: 5, phone_number: '+254734567890', name: 'Faith Muthoni', county: 'Nyeri', created_at: '2025-11-20' },
  { id: 6, phone_number: '+254745678901', name: 'David Kiprop', county: 'Uasin Gishu', created_at: '2025-12-05' },
  { id: 7, phone_number: '+256772345678', name: 'Sarah Auma', county: 'Gulu', created_at: '2026-01-10' },
  { id: 8, phone_number: '+255723456789', name: 'Rehema Said', county: 'Mwanza', created_at: '2026-01-25' },
];

export const mockReservations = [
  { id: 1, user_id: 1, book_id: 1, reserved_at: '2026-02-10', due_date: '2026-02-24', returned: false },
  { id: 2, user_id: 2, book_id: 5, reserved_at: '2026-02-12', due_date: '2026-02-26', returned: false },
  { id: 3, user_id: 3, book_id: 2, reserved_at: '2026-02-08', due_date: '2026-02-22', returned: true },
  { id: 4, user_id: 5, book_id: 7, reserved_at: '2026-02-15', due_date: '2026-03-01', returned: false },
  { id: 5, user_id: 4, book_id: 8, reserved_at: '2026-02-05', due_date: '2026-02-19', returned: true },
  { id: 6, user_id: 6, book_id: 9, reserved_at: '2026-02-18', due_date: '2026-03-04', returned: false },
  { id: 7, user_id: 7, book_id: 4, reserved_at: '2026-02-20', due_date: '2026-03-06', returned: false },
  { id: 8, user_id: 1, book_id: 5, reserved_at: '2026-01-20', due_date: '2026-02-03', returned: true },
];

export const mockStats = {
  totalUsers: 8,
  totalBooks: 10,
  activeReservations: 5,
  totalSessions: 342,
  smsSent: 1287,
  booksSearched: 856,
};
