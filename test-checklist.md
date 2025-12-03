# KMNR Website Testing Checklist

## Application Status
- ✅ Frontend: Running on http://localhost:4200
- ✅ Database: Running on localhost:3306
- ⚠️  Backend: Running on localhost:5000 (some issues with endpoints)

## Visual Layout Tests

### 1. Homepage (/)
- [ ] Background image displays properly
- [ ] Modular cards with white tinted background show
- [ ] Navigation bar shows with SpecialElite font in uppercase
- [ ] "KMNR" link in navigation instead of "home"
- [ ] Featured playlist section displays
- [ ] No purple navigation bar visible

### 2. About Page (/about)
- [ ] Background image displays properly
- [ ] Content wrapped in modular card with white tinted background
- [ ] All text readable on tinted background
- [ ] Navigation functioning

### 3. Shows Page (/shows)
- [ ] Background image displays properly
- [ ] Schedule content wrapped in modular card
- [ ] Navigation functioning

### 4. Blog Page (/blog)
- [ ] Background image displays properly
- [ ] Blog content wrapped in modular card
- [ ] Navigation functioning

### 5. News Page (/news)
- [ ] Background image displays properly
- [ ] News content wrapped in modular card
- [ ] Navigation functioning

### 6. DJs Page (/djs)
- [ ] Background image displays properly
- [ ] DJ list wrapped in modular card
- [ ] Navigation functioning

### 7. Spotify Page (/spotify)
- [ ] Background image displays properly
- [ ] Content wrapped in modular card
- [ ] Navigation functioning

## Navigation Tests

### Desktop Navigation
- [ ] Black navigation bar displays
- [ ] SpecialElite font loads correctly
- [ ] All text is uppercase
- [ ] "KMNR" link navigates to homepage
- [ ] All navigation links work
- [ ] Hover effects work (yellow glow)
- [ ] Active state highlighting works

### Mobile Navigation (resize window < 768px)
- [ ] Desktop navigation hides
- [ ] Mobile header shows with "kmnr" and "menu" button
- [ ] Menu button opens overlay
- [ ] Mobile navigation links work
- [ ] Overlay closes when clicking outside or on links

## Styling Tests

### Background System
- [ ] Background image loads on all pages
- [ ] Background is fixed and covers entire viewport
- [ ] Background doesn't scroll with content

### Modular Card System
- [ ] White tinted background (rgba(255, 255, 255, 0.95))
- [ ] Rounded corners (16px border-radius)
- [ ] Box shadow visible
- [ ] Backdrop blur effect
- [ ] Hover effects work (translateY and enhanced shadow)
- [ ] Proper spacing and margins

### Typography
- [ ] SpecialElite font loads for navigation
- [ ] Original fonts preserved for content (Bree Serif, Roboto Condensed, etc.)
- [ ] Text is readable on all backgrounds

## Functional Tests

### Featured Playlist Section
- [ ] Section displays on homepage
- [ ] Styled with Spotify colors (green and dark gray)
- [ ] "Open in Spotify" button present
- [ ] Button has proper Spotify styling

### Responsive Design
- [ ] All pages responsive on desktop
- [ ] All pages responsive on tablet
- [ ] All pages responsive on mobile
- [ ] Mobile navigation works properly

## Technical Tests

### Compilation
- [ ] No TypeScript errors
- [ ] No Angular warnings
- [ ] Clean build output

### Performance
- [ ] Pages load quickly
- [ ] Navigation is smooth
- [ ] No console errors in browser dev tools

## Cross-Browser Testing (if possible)
- [ ] Chrome
- [ ] Firefox  
- [ ] Safari

## Issues Found
[Document any issues discovered during testing]

## Test Results Summary
[To be filled after testing]