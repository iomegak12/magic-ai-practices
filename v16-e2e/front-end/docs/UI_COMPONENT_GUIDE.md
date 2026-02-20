# UI Component Guide

**Version:** 1.0.0  
**Last Updated:** February 20, 2026

## Table of Contents

- [Overview](#overview)
- [Design System](#design-system)
- [Chat Interface](#chat-interface)
- [Session Management](#session-management)
- [Error Displays](#error-displays)
- [Loading States](#loading-states)
- [Tool Call Indicators](#tool-call-indicators)
- [Form Components](#form-components)
- [Navigation](#navigation)
- [Data Tables](#data-tables)
- [Modals and Dialogs](#modals-and-dialogs)
- [Accessibility Guidelines](#accessibility-guidelines)

---

## Overview

This guide provides high-level recommendations for UI components based on Tabler Admin Template. All recommendations focus on user experience patterns rather than implementation code.

### UI Framework: Tabler Admin Template

**Version**: Latest (Free Edition)  
**Source**: CDN  
**Documentation**: https://tabler.io/docs

**Key Features**:
- Responsive design out of the box
- Modern Bootstrap 5 based
- Clean and minimal interface
- Comprehensive component library
- Dark mode support

---

## Design System

### Color Palette

**Primary Colors** (Indigo Blue & White theme):
- **Primary**: Indigo (#6366f1) - Actions, links, primary buttons
- **Primary Light**: Indigo 400 (#818cf8) - Hover states, accents
- **Primary Dark**: Indigo 600 (#4f46e5) - Active states, emphasis
- **Success**: Green (#2fb344) - Success states, confirmations
- **Warning**: Orange (#f76707) - Warnings, rate limit indicators
- **Danger**: Red (#d63939) - Errors, destructive actions
- **Info**: Cyan (#4299e1) - Information, tips
- **Secondary**: Gray (#6c757d) - Secondary actions, disabled states

**Theme Support** (Dark/Light Mode):
- **Light Background**: White (#ffffff)
- **Light Surface**: Light Gray (#f8f9fa)
- **Light Text**: Dark Gray (#1e293b)  
- **Dark Background**: Dark Gray (#0f172a)
- **Dark Surface**: Slate (#1e293b)
- **Dark Text**: Light Gray (#f1f5f9)

**Semantic Colors**:
- **User Message**: Light indigo background (#e0e7ff) / Dark indigo background (#312e81)
- **Assistant Message**: Light gray background (#f1f5f9) / Dark gray background (#334155)
- **System Message**: Yellow-tinted background (#fef3c7) / Dark yellow background (#713f12)
- **Tool Execution**: Purple-tinted background (#f3e8ff) / Dark purple background (#581c87)

### Typography

**Font Family**: Inter (Tabler default)

**Scale**:
- H1: 2rem (32px) - Page titles
- H2: 1.5rem (24px) - Section headers
- H3: 1.25rem (20px) - Card headers
- Body: 0.875rem (14px) - Main content
- Small: 0.75rem (12px) - Helper text, timestamps

### Spacing

Follow 8px grid system:
- **4px**: Tight spacing (icons, badges)
- **8px**: Small spacing (form elements)
- **16px**: Medium spacing (component padding)
- **24px**: Large spacing (component margins)
- **32px**: Extra large spacing (section spacing)

---

## Chat Interface

### Layout Structure

```
┌─────────────────────────────────────────┐
│  Chat Header                            │
│  [Session Title] [Actions]              │
├─────────────────────────────────────────┤
│                                         │
│  Message List (scrollable)              │
│                                         │
│  ┌─────────────────────────────┐       │
│  │ User Message                │       │
│  └─────────────────────────────┘       │
│       ┌─────────────────────────────┐  │
│       │ Assistant Message           │  │
│       │ [Tool Call: Searching...]   │  │
│       └─────────────────────────────┘  │
│                                         │
├─────────────────────────────────────────┤
│  Message Input                          │
│  [Textarea] [Send] [☰ Options]          │
└─────────────────────────────────────────┘
```

### Chat Header

**Components**:
- **Session Title**: H3 header, editable inline
- **Status Indicator**: Dot (green=connected, yellow=connecting, red=disconnected)
- **Session ID**: Small, muted text
- **Action Buttons**:
  - Clear history
  - Export conversation
  - Settings
  - Close session

**Behavior**:
- Sticky position when scrolling
- Collapse on mobile to save space
- Show last activity time

### Message List

**Recommendations**:

1. **Auto-scroll**: Always scroll to bottom when new message arrives
2. **Scroll Indicator**: Show "↓ New message" button when user scrolled up
3. **Virtual Scrolling**: For conversations with 100+ messages
4. **Lazy Loading**: Load older messages on scroll to top
5. **Grouping**: Group messages by time (Today, Yesterday, Last Week)

**Message Bubble Design**:

**User Messages** (right-aligned):
- Light blue background (`bg-primary-lt`)
- Dark text
- User avatar (top-right)
- Timestamp below (small, muted)
- Checkmark icon (sent/delivered/read)

**Assistant Messages** (left-aligned):
- Light gray background (`bg-light`)
- Dark text
- Bot avatar (top-left)
- Timestamp below
- Action buttons (Copy, Regenerate, Feedback)

**System Messages** (centered):
- Yellow-tinted background
- Smaller font size
- Icon prefix (ℹ️ for info, ⚠️ for warnings)
- Full width, centered text

### Message Input

**Components**:

1. **Textarea**:
   - Auto-resize (min 2 rows, max 10 rows)
   - Placeholder: "Type your message... (Shift+Enter for new line)"
   - Character counter when approaching limit (4800/5000)
   - Emoji picker button
   - File attachment button (future)

2. **Send Button**:
   - Primary color
   - Disabled when empty or sending
   - Show spinner when loading
   - Keyboard shortcut: Enter

3. **Options Dropdown**:
   - Toggle streaming mode
   - Change model (future)
   - Adjust temperature (future)
   - Clear input

**Behavior**:
- Sticky at bottom
- Expand input on focus
- Save draft in localStorage
- Show typing indicator when assistant is typing

### Typing Indicator

**Design**:
- Three animated dots (⋯)
- Light gray background
- Small size (16px height)
- Position: Below last message
- Animation: Pulse effect

**States**:
- **Idle**: Hidden
- **Typing**: Show with animation
- **Tool Executing**: Show "🔧 Using tool: [tool name]..."
- **Streaming**: Show "✍️ Generating response..."

---

## Session Management

### Session Selector (Support Page)

**Layout** (Displayed on Support page, not sidebar):
```
┌──────────────────────┐
│ + New Chat           │ (Primary button)
├──────────────────────┤
│ 🔍 Search sessions   │ (Search input)
├──────────────────────┤
│ Today                │ (Section header)
│  ┌────────────────┐  │
│  │ [Session 1]    │  │ (Active)
│  │ 10:30 AM       │  │
│  │ "How do I..."  │  │
│  └────────────────┘  │
│  ┌────────────────┐  │
│  │ [Session 2]    │  │
│  │ 09:15 AM       │  │
│  │ "Order status" │  │
│  └────────────────┘  │
├──────────────────────┤
│ Yesterday            │
│  [Sessions...]       │
├──────────────────────┤
│ Last 7 Days          │
│  [Sessions...]       │
└──────────────────────┘
```

**Alternative Layout**: Dropdown selector in Support page header:
```
┌─────────────────────────────────────────┐
│ Select Session: [Session 1 - 10:30 AM] ▼│
└─────────────────────────────────────────┘
```

**Session Item Components**:
- **Avatar**: User icon or custom
- **Title**: First message preview (truncated)
- **Timestamp**: Relative time (2 minutes ago, 1 hour ago)
- **Message Count**: Badge (12 messages)
- **Hover Actions**:
  - Pin session
  - Rename session
  - Delete session
  - Share session

**Behavior**:
- Highlight active session
- Drag to reorder (future)
- Right-click context menu
- Infinite scroll for old sessions

### Session Filter

**Filter Options**:
- **Time Range**: Today, This Week, This Month, All Time
- **Tenant**: Dropdown (if multi-tenant)
- **Message Count**: Range slider (1-100+)
- **Has Tool Calls**: Checkbox
- **Sort By**: Recent, Oldest, Most Messages, Least Messages

**UI Pattern**:
- Collapsible filter panel
- Apply/Reset buttons
- Show active filters as tags
- Clear all filters button

### Session Stats Dashboard

**Metrics Cards**:

1. **Total Sessions**: Big number with trend (↑ 12% this week)
2. **Active Sessions**: Count with last activity
3. **Average Messages**: Per session
4. **Tool Usage**: Count of tool calls

**Charts**:
- **Sessions Over Time**: Line chart (last 30 days)
- **Sessions by Tenant**: Pie chart
- **Message Distribution**: Bar chart (0-10, 11-20, 21-50, 50+)
- **Peak Hours**: Heatmap (day vs hour)

**Components** (Tabler):
- Use `.card` for metric cards
- Use Chart.js or ApexCharts for visualizations
- Use `.badge` for trend indicators

---

## Error Displays

### Toast Notifications

**Types**:

1. **Success** (green):
   - Icon: ✓
   - Title: "Success"
   - Message: "Session created successfully"
   - Duration: 3 seconds
   - Dismissible: Yes

2. **Error** (red):
   - Icon: ✕
   - Title: "Error"
   - Message: "Failed to send message. Please try again."
   - Duration: 5 seconds
   - Dismissible: Yes
   - Action button: "Retry"

3. **Warning** (orange):
   - Icon: ⚠
   - Title: "Warning"
   - Message: "Approaching rate limit (45/50 requests)"
   - Duration: 5 seconds
   - Dismissible: Yes

4. **Info** (blue):
   - Icon: ℹ
   - Title: "Info"
   - Message: "New version available. Refresh to update."
   - Duration: Until dismissed
   - Action button: "Refresh"

**Position**: Top-right corner  
**Stack**: Show up to 3 toasts, oldest at bottom  
**Animation**: Slide in from right, fade out

### Error Boundary Fallback

**Full Page Error**:
```
┌─────────────────────────────────────┐
│                                     │
│         😞                          │
│                                     │
│    Oops! Something went wrong       │
│                                     │
│  We're sorry, but something         │
│  unexpected happened.               │
│                                     │
│  [Reload Page] [Report Issue]      │
│                                     │
│  > Show technical details           │
│    (collapsed by default)           │
└─────────────────────────────────────┘
```

**Component Error** (partial):
- Show error message inline
- Provide retry button
- Log error to console
- Send to error tracking (future)

### Inline Validation Errors

**Form Fields**:
- Red border on invalid field
- Error icon (✕) on right
- Error message below field (small, red)
- Shake animation on submit with errors

**Example Messages**:
- "Message cannot be empty"
- "Message too long (5,245 / 5,000 characters)"
- "Session ID is required"
- "Invalid tenant format"

---

## Loading States

### Skeleton Screens

**Message List Skeleton**:
```
┌─────────────────────────────────┐
│ ░░░░░░░░░░░ (gray shimmer)      │
│ ░░░░░░░░░░░░░░                  │
│                                 │
│      ░░░░░░░░░░░░░░░░░░░░░░    │
│      ░░░░░░░░░░░                │
└─────────────────────────────────┘
```

**Session List Skeleton**:
```
┌──────────────────┐
│ ░░░░░░░░░░░░░░  │
│ ░░░░░░          │
├──────────────────┤
│ ░░░░░░░░░░░░░░  │
│ ░░░░░░          │
├──────────────────┤
│ ░░░░░░░░░░░░░░  │
│ ░░░░░░          │
└──────────────────┘
```

**Behavior**:
- Shimmer animation (left to right)
- Match actual component dimensions
- Show for minimum 300ms (avoid flashing)
- Fade transition to real content

### Spinners

**Use Cases**:
1. **Button Loading**: Small spinner replacing button text
2. **Page Loading**: Large spinner centered on page
3. **Inline Loading**: Small spinner next to text ("Loading messages...")
4. **Overlay Loading**: Full-screen with backdrop

**Types** (Tabler):
- `.spinner-border`: Circular spinner
- `.spinner-grow`: Growing dots

**Sizes**:
- `sm`: 16px (buttons)
- `md`: 32px (cards)
- `lg`: 64px (page)

### Progress Bars

**Use Cases**:
1. **File Upload**: Show percentage (45% uploaded)
2. **Long Operation**: Show progress (Processing: 3/10 items)
3. **Rate Limit**: Show remaining capacity (45/50 requests)

**Components** (Tabler):
- `.progress` with `.progress-bar`
- Animate width change
- Show percentage label
- Color coding (success=green, warning=orange, danger=red)

---

## Tool Call Indicators

### Tool Call Badge

**Design**:
- Small badge above assistant message
- Icon: 🔧 or tool-specific icon
- Text: "Using [Tool Name]"
- Background: Purple-tinted
- Border: Dotted (while executing), Solid (completed)

**States**:

1. **Executing**:
   - Animated spinner
   - Text: "🔧 Searching orders..."
   - Pulsing animation

2. **Completed**:
   - Checkmark icon: ✓
   - Text: "✓ Searched orders"
   - Static, solid border

3. **Failed**:
   - Error icon: ✕
   - Text: "✕ Failed to search orders"
   - Red border and text

### Tool Result Display

**Collapsed (default)**:
```
┌─────────────────────────────────┐
│ ✓ Searched orders (2 results)   │
│   > Show details                │
└─────────────────────────────────┘
```

**Expanded**:
```
┌─────────────────────────────────┐
│ ✓ Searched orders (2 results)   │
│   ∨ Hide details                │
│                                 │
│ Tool: search_orders             │
│ Duration: 1.2s                  │
│ Parameters:                     │
│   - customer_id: 12345          │
│   - status: pending             │
│                                 │
│ Results:                        │
│   [Order #1001] $125.00         │
│   [Order #1002] $75.50          │
└─────────────────────────────────┘
```

**Behavior**:
- Click to toggle expand/collapse
- Syntax highlighting for JSON
- Copy button for raw result
- Link to full details (if available)

---

## Form Components

### Input Fields

**Text Input**:
- Label above
- Helper text below (muted, small)
- Optional indicator: (optional)
- Required indicator: * (red)
- Max length indicator when typing

**Textarea**:
- Auto-resize
- Character counter
- Resize handle (optional)

**Select/Dropdown**:
- Searchable for 10+ options
- Clear button (×)
- Multi-select with tags
- Custom option template

**Checkbox/Radio**:
- Large touch targets (44x44px)
- Clear labels
- Helper text below
- Group related options

### Buttons

**Types**:
1. **Primary**: Main action (Create, Send, Save)
2. **Secondary**: Alternative action (Cancel, Back)
3. **Danger**: Destructive action (Delete, Remove)
4. **Link**: Text only (Learn more, View details)

**States**:
- Default
- Hover (slight darken)
- Active (pressed)
- Disabled (gray, cursor not-allowed)
- Loading (spinner, disabled)

**Sizes**:
- Small: 32px height
- Medium: 40px height
- Large: 48px height

### Form Validation

**Inline Validation**:
- Validate on blur (not on every keystroke)
- Show error immediately
- Clear error when fixed
- Visual feedback (color, icon, message)

**Submit Validation**:
- Prevent submit if errors
- Scroll to first error
- Focus first invalid field
- Shake animation

---

## Navigation

### Top Navigation Bar

**Layout**:
```
┌────────────────────────────────────────────────────────────┐
│ [Logo] Home | About Us | Contact Us | Support | Settings   │
│                         [Tenant ▼] [🌙/☀️] [User ▼]        │
└────────────────────────────────────────────────────────────┘
```

**Components**:
- **Logo**: Left corner, clickable (home link)
- **Navigation Menu**: Horizontal menu items
  - **Home**: Landing/dashboard page
  - **About Us**: Company information page
  - **Contact Us**: Contact form page
  - **Support**: Chat interface (main feature)
  - **Settings**: User preferences and configuration
- **Right Actions**:
  - **Tenant Selector**: Dropdown (multi-tenancy)
  - **Theme Toggle**: Sun/Moon icon (dark/light mode)
  - **User Menu**: Avatar with dropdown (profile, logout)

**States**:
- **Default**: All items visible
- **Active**: Highlighted with indigo underline/background (#6366f1)
- **Hover**: Light indigo background (#e0e7ff)

**Desktop Behavior** (>768px):
- Full horizontal layout
- Sticky position (remains at top)
- All menu items visible
- Hover effects enabled

**Mobile Behavior** (<768px):
- Logo + hamburger menu icon (☰)
- Tap hamburger to reveal menu
- Menu slides in from right or drops down
- Close button (✕) to dismiss

**Theme Toggle**:
- **Light Mode**: ☀️ Sun icon, switches to dark mode onClick
- **Dark Mode**: 🌙 Moon icon, switches to light mode onClick
- Persisted in localStorage
- Applies theme change globally

### Breadcrumbs

**Pattern**:
```
Home / Support / Session #12345 / History
```

**Behavior**:
- Show hierarchical position
- Clickable parent levels
- Current page (last) is not clickable
- Truncate middle levels on mobile

### Tabs

**Use Cases**:
- Settings page: Theme, Tenant, Preferences
- Support page: Current Session, History, Quick Actions

**Pattern** (Tabler):
- Use `.nav-tabs` or `.nav-pills`
- Active tab highlighted with indigo (#6366f1)
- Underline indicator (tabs) or background (pills)
- Scroll horizontal on mobile

---

## Data Tables

### Sessions Table

**Columns**:
1. Session ID (link, truncated)
2. Tenant (badge)
3. Created (relative time)
4. Last Activity (relative time)
5. Messages (count)
6. Status (badge: active, expired, deleted)
7. Actions (dropdown: View, Delete, Export)

**Features**:
- **Sort**: Click column header
- **Filter**: Search box above table
- **Pagination**: 10, 25, 50, 100 per page
- **Selection**: Checkbox for bulk actions
- **Responsive**: Stack on mobile (card view)

**Empty State**:
```
┌─────────────────────────────────┐
│                                 │
│        📭                       │
│                                 │
│    No sessions found            │
│                                 │
│  Create your first session to   │
│  get started.                   │
│                                 │
│  [+ New Session]                │
└─────────────────────────────────┘
```

### Message History Table

**Columns**:
1. Timestamp
2. Role (user/assistant/system)
3. Message (truncated, expandable)
4. Tool Calls (count, link)
5. Actions (View full, Copy)

**Features**:
- Expandable rows for full message
- Syntax highlighting for code
- Copy button for each message
- Export conversation (JSON, CSV, PDF)

---

## Modals and Dialogs

### Confirmation Dialog

**Delete Session**:
```
┌─────────────────────────────────┐
│ Delete Session?              × │
├─────────────────────────────────┤
│                                 │
│ Are you sure you want to delete │
│ this session?                   │
│                                 │
│ • All messages will be lost     │
│ • This action cannot be undone  │
│                                 │
│ Session: #sess_abc123           │
│ Messages: 24                    │
│                                 │
│         [Cancel] [Delete]       │
└─────────────────────────────────┘
```

**Behavior**:
- Backdrop (semi-transparent black)
- Center on screen
- Close on ESC key
- Close on backdrop click (optional)
- Focus trap (keyboard navigation)
- Danger action disabled for 2 seconds (prevent accidental)

### Form Dialog

**Create Session**:
```
┌─────────────────────────────────┐
│ Create New Session           × │
├─────────────────────────────────┤
│                                 │
│ Session ID (optional)           │
│ [____________]                  │
│                                 │
│ Tenant                          │
│ [default        ▼]              │
│                                 │
│ Metadata (optional)             │
│ [____________]                  │
│                                 │
│         [Cancel] [Create]       │
└─────────────────────────────────┘
```

### Alert Dialog

**Rate Limit Warning**:
```
┌─────────────────────────────────┐
│ ⚠ Rate Limit Warning         × │
├─────────────────────────────────┤
│                                 │
│ You have used 48 of 50 requests │
│ in the last minute.             │
│                                 │
│ Please wait before sending more │
│ requests.                       │
│                                 │
│ Time until reset: 42 seconds    │
│                                 │
│              [OK]               │
└─────────────────────────────────┘
```

---

## Accessibility Guidelines

### Keyboard Navigation

**Required Shortcuts**:
- **Tab**: Navigate between interactive elements
- **Shift+Tab**: Navigate backwards
- **Enter**: Activate button/link
- **Space**: Toggle checkbox, activate button
- **ESC**: Close modal/dropdown
- **Arrow Keys**: Navigate menu items, tabs

**Custom Shortcuts**:
- **Ctrl+Enter**: Send message
- **Ctrl+K**: Focus search
- **Ctrl+N**: New session
- **Ctrl+/**: Show keyboard shortcuts

### Screen Reader Support

**ARIA Labels**:
```
<button aria-label="Send message">
  <span aria-hidden="true">➤</span>
</button>

<div role="status" aria-live="polite">
  Message sent successfully
</div>

<input
  type="text"
  aria-required="true"
  aria-invalid="true"
  aria-describedby="error-message"
/>
```

**Semantic HTML**:
- Use `<button>` for buttons (not `<div>`)
- Use `<nav>` for navigation
- Use `<main>` for main content
- Use `<header>`, `<footer>` for sections
- Use `<form>` for forms

### Color Contrast

**WCAG AA Requirements**:
- Normal text: 4.5:1 contrast ratio
- Large text (18pt+): 3:1 contrast ratio
- UI components: 3:1 contrast ratio

**Testing**:
- Use browser DevTools
- Use contrast checker tools
- Test with different color blindness filters

### Focus Indicators

**Requirements**:
- All interactive elements must have visible focus
- Focus indicator minimum 2px thick
- High contrast (3:1 ratio)
- Not hidden by CSS (`outline: none` forbidden)

**Tabler Default** (Customized for Indigo theme):
- Indigo outline (`--primary-color: #6366f1`)
- Offset 2px from element
- Visible on all interactive elements

---

## Responsive Design

### Breakpoints

- **xs**: 0-575px (mobile portrait)
- **sm**: 576-767px (mobile landscape)
- **md**: 768-991px (tablet)
- **lg**: 992-1199px (desktop)
- **xl**: 1200-1399px (large desktop)
- **xxl**: 1400px+ (extra large)

### Mobile Adaptations

**Chat Interface** (Support page):
- Collapse top navigation to hamburger menu
- Full-width chat area
- Simplify header (just session title)
- Larger touch targets (min 44x44px)
- Bottom action bar for message input

**Tables**:
- Convert to card view
- Stack columns vertically
- Show most important columns only
- Expandable rows for details

**Forms**:
- Full width inputs
- Larger buttons (48px height)
- Stack buttons vertically
- Auto-focus first field (except mobile)

---

## Summary

This UI guide provides:

✅ **Design System**: Colors, typography, spacing  
✅ **Chat Interface**: Message list, input, typing indicators  
✅ **Session Management**: List, filters, stats  
✅ **Error Displays**: Toasts, boundaries, validation  
✅ **Loading States**: Skeletons, spinners, progress  
✅ **Tool Indicators**: Badges, results, animations  
✅ **Forms**: Inputs, validation, buttons  
✅ **Navigation**: Top navbar with theme toggle, breadcrumbs  
✅ **Tables**: Sessions, messages, pagination  
✅ **Modals**: Confirmations, forms, alerts  
✅ **Accessibility**: Keyboard, screen readers, contrast

---

## Resources

- **Tabler Documentation**: https://tabler.io/docs
- **Tabler Components**: https://tabler.io/docs/components
- **Tabler Icons**: https://tabler-icons.io
- **Bootstrap 5 Docs**: https://getbootstrap.com/docs/5.0
- **WCAG Guidelines**: https://www.w3.org/WAI/WCAG21/quickref

For implementation details, see:
- [Frontend Architecture](./FRONTEND_ARCHITECTURE.md)
- [Project Structure](./PROJECT_STRUCTURE.md)
