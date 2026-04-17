import {
  isToday,
  isYesterday,
  differenceInDays,
  parseISO,
} from 'date-fns';

/**
 * Groups an object of sessions into date-based buckets for the sidebar.
 * Returns an array of { label, sessions } sorted newest-first.
 */
export function groupChatsByDate(sessions) {
  const groups = {
    Today: [],
    Yesterday: [],
    'Previous 7 Days': [],
    Older: [],
  };

  const list = Object.values(sessions).sort(
    (a, b) => new Date(b.updatedAt) - new Date(a.updatedAt)
  );

  const now = new Date();

  for (const session of list) {
    const date = parseISO(session.updatedAt || session.createdAt);

    if (isToday(date)) {
      groups['Today'].push(session);
    } else if (isYesterday(date)) {
      groups['Yesterday'].push(session);
    } else if (differenceInDays(now, date) <= 7) {
      groups['Previous 7 Days'].push(session);
    } else {
      groups['Older'].push(session);
    }
  }

  return Object.entries(groups)
    .filter(([, items]) => items.length > 0)
    .map(([label, items]) => ({ label, sessions: items }));
}
