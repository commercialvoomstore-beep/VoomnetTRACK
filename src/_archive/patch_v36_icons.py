#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3.6 — Tous les symboles redessinés en duotone « objet réel » (volumes + remplissages + accents)."""

ICONS = {
# ---- navigation / espaces ----
"grid": '<rect x="3" y="3" width="8" height="8" rx="2.6" fill="currentColor" fill-opacity=".18"/><rect x="13" y="3" width="8" height="8" rx="2.6"/><rect x="3" y="13" width="8" height="8" rx="2.6"/><rect x="13" y="13" width="8" height="8" rx="2.6" fill="currentColor" fill-opacity=".18"/><path d="M5.6 7h2.8M5.6 17h2.8M15.6 7h2.8M15.6 17h2.8" stroke-width="1.3" stroke-opacity=".5"/>',
"list": '<rect x="4.4" y="4.2" width="15.2" height="16.8" rx="2.6" fill="currentColor" fill-opacity=".14"/><path d="M4.4 8.4h15.2" /><path d="M9 4.2h6v2.6a1.3 1.3 0 0 1-1.3 1.3h-3.4A1.3 1.3 0 0 1 9 6.8z" fill="currentColor" fill-opacity=".42"/><rect x="4.4" y="4.2" width="15.2" height="16.8" rx="2.6"/><path d="M8 11.8h8M8 14.8h8M8 17.8h4.6" stroke-width="1.6"/>',
"chart": '<path d="M3.4 20.6h17.2" stroke-width="1.7"/><rect x="5.2" y="12.4" width="3.8" height="6.8" rx="1.3" fill="currentColor" fill-opacity=".22"/><rect x="10.1" y="7" width="3.8" height="12.2" rx="1.3" fill="currentColor" fill-opacity=".44"/><rect x="15" y="14.8" width="3.8" height="4.4" rx="1.3" fill="currentColor" fill-opacity=".22"/><rect x="5.2" y="12.4" width="3.8" height="6.8" rx="1.3"/><rect x="10.1" y="7" width="3.8" height="12.2" rx="1.3"/><rect x="15" y="14.8" width="3.8" height="4.4" rx="1.3"/>',
"doc": '<path d="M6.2 3.4h7.2l5.2 5.2V19a1.9 1.9 0 0 1-1.9 1.9H6.2A1.9 1.9 0 0 1 4.3 19V5.3A1.9 1.9 0 0 1 6.2 3.4z" fill="currentColor" fill-opacity=".13"/><path d="M13.4 3.4v3.8a1.4 1.4 0 0 0 1.4 1.4h3.8" fill="currentColor" fill-opacity=".34"/><path d="M6.2 3.4h7.2l5.2 5.2V19a1.9 1.9 0 0 1-1.9 1.9H6.2A1.9 1.9 0 0 1 4.3 19V5.3A1.9 1.9 0 0 1 6.2 3.4z"/><path d="M7.8 12.6h7M7.8 15.8h7M7.8 18.8h4" stroke-width="1.6"/>',
"car": '<path d="M3.6 15.8v-1.4c0-.7.4-1.4 1-1.8l1.6-.9 1.7-3.1a2.6 2.6 0 0 1 2.3-1.4h3.6a2.6 2.6 0 0 1 2.3 1.4l1.7 3.1 1.6.9c.6.4 1 1.1 1 1.8v1.4z" fill="currentColor" fill-opacity=".16"/><path d="M3.6 15.8v-1.4c0-.7.4-1.4 1-1.8l1.6-.9 1.7-3.1a2.6 2.6 0 0 1 2.3-1.4h3.6a2.6 2.6 0 0 1 2.3 1.4l1.7 3.1 1.6.9c.6.4 1 1.1 1 1.8v1.4"/><path d="M7.6 11.4h8.8" stroke-width="1.4"/><path d="M4.6 15.8v1.4a1 1 0 0 0 1 1h.6a1 1 0 0 0 1-1v-1.4M16.8 15.8v1.4a1 1 0 0 0 1 1h.6a1 1 0 0 0 1-1v-1.4"/><circle cx="8.4" cy="16" r="2.1" fill="#fff"/><circle cx="15.6" cy="16" r="2.1" fill="#fff"/><circle cx="8.4" cy="16" r="2.1"/><circle cx="15.6" cy="16" r="2.1"/><circle cx="8.4" cy="16" r=".8" fill="currentColor" stroke="none"/><circle cx="15.6" cy="16" r=".8" fill="currentColor" stroke="none"/><path d="M19.6 12.6h1" stroke-width="1.7"/>',
"users": '<circle cx="9.4" cy="8.6" r="3.5" fill="currentColor" fill-opacity=".24"/><path d="M3.2 19.8a6.2 6.2 0 0 1 12.4 0z" fill="currentColor" fill-opacity=".24"/><circle cx="9.4" cy="8.6" r="3.5"/><path d="M3.2 19.8a6.2 6.2 0 0 1 12.4 0"/><path d="M16.4 5.9a2.9 2.9 0 0 1 0 5.6" stroke-width="1.7"/><path d="M17.8 19.8a5.4 5.4 0 0 0-1.1-3.2 4.6 4.6 0 0 1 3.9 2.4" stroke-width="1.7"/>',
"settings": '<circle cx="12" cy="12" r="3.1" fill="currentColor" fill-opacity=".55"/><path d="M10.2 2.9h3.6l.5 2.2 1.9.8 1.9-1.2 2.5 2.5-1.2 1.9.8 1.9 2.2.5v3.6l-2.2.5-.8 1.9 1.2 1.9-2.5 2.5-1.9-1.2-1.9.8-.5 2.2h-3.6l-.5-2.2-1.9-.8-1.9 1.2-2.5-2.5 1.2-1.9-.8-1.9-2.2-.5v-3.6l2.2-.5.8-1.9-1.2-1.9 2.5-2.5 1.9 1.2 1.9-.8z" fill="currentColor" fill-opacity=".14"/><circle cx="12" cy="12" r="8.4"/><circle cx="12" cy="12" r="3.1"/>',
# ---- actions ----
"plus": '<circle cx="12" cy="12" r="8.6" fill="currentColor" fill-opacity=".13"/><path d="M12 7.6v8.8M7.6 12h8.8" stroke-width="2"/>',
"menu": '<path d="M4 7.4h16M4 12h16M4 16.6h11" stroke-width="2"/>',
"search": '<circle cx="10.8" cy="10.8" r="6.6" fill="currentColor" fill-opacity=".13"/><circle cx="10.8" cy="10.8" r="6.6" stroke-width="1.9"/><path d="M15.8 15.8 20.4 20.4" stroke-width="2.1" stroke-linecap="round"/>',
"bell": '<path d="M12 3.4a5.6 5.6 0 0 1 5.6 5.6c0 4 1.4 5.2 1.4 5.2H5s1.4-1.2 1.4-5.2A5.6 5.6 0 0 1 12 3.4z" fill="currentColor" fill-opacity=".18"/><path d="M12 3.4a5.6 5.6 0 0 1 5.6 5.6c0 4 1.4 5.2 1.4 5.2H5s1.4-1.2 1.4-5.2A5.6 5.6 0 0 1 12 3.4z"/><path d="M9.9 17.6a2.2 2.2 0 0 0 4.2 0" stroke-width="1.8"/>',
"chevDown": '<path d="m6.6 9.4 5.4 5.4 5.4-5.4" stroke-width="2.1"/>',
"wallet": '<rect x="3.2" y="6.8" width="17.6" height="11.4" rx="2.9" fill="currentColor" fill-opacity=".14"/><path d="M3.2 9.6h17.6v2.6H3.2z" fill="currentColor" fill-opacity=".32"/><rect x="3.2" y="6.8" width="17.6" height="11.4" rx="2.9"/><rect x="13.8" y="11.4" width="7" height="4.2" rx="1.5" fill="currentColor" fill-opacity=".26"/><circle cx="16.9" cy="13.5" r="1.05" fill="currentColor" stroke="none"/><path d="M7.4 13.8h3.6" stroke-width="1.5" stroke-opacity=".55"/><circle cx="18.4" cy="5.2" r="2.6" fill="var(--accent)" fill-opacity=".2" stroke="var(--accent)" stroke-width="1.4"/><path d="M18.4 4.2v2" stroke="var(--accent)" stroke-width="1.4"/>',
"route": '<path d="M4.8 19.4h3.4a3 3 0 0 0 3-3v-3.6a3 3 0 0 1 3-3h2.6" fill="none" stroke-dasharray="2.4 2.4" stroke-width="1.7"/><circle cx="4.6" cy="19.4" r="1.9" fill="currentColor"/><path d="M17.2 15.2c-1.9 0-3.4-1.5-3.4-3.4s1.5-3.4 3.4-3.4 3.4 1.5 3.4 3.4c0 2.2-2.3 4.5-3.4 5.7z" fill="var(--accent)" fill-opacity=".2" stroke="var(--accent)" stroke-width="1.4"/><circle cx="17.2" cy="11.8" r="1.15" fill="var(--accent)" stroke="none"/>',
"trend": '<path d="M3.4 20.6h17.2" stroke-width="1.6"/><path d="M4.4 16.4 9 11.4l3.4 2.8 6.6-7.6" stroke-width="2"/><path d="M19 6.6h-4.6M19 6.6v4.4" stroke-width="2"/>',
"bolt": '<path d="M13.4 2.8 5.6 13.4h5.2l-1.2 7.8 8.2-10.8h-5.4z" fill="var(--accent)" fill-opacity=".22" stroke="var(--accent)" stroke-width="1.6" stroke-linejoin="round"/>',
"alert": '<path d="M12 3.6 21.2 19.4a1.6 1.6 0 0 1-1.4 2.4H4.2a1.6 1.6 0 0 1-1.4-2.4z" fill="currentColor" fill-opacity=".14"/><path d="M12 3.6 21.2 19.4a1.6 1.6 0 0 1-1.4 2.4H4.2a1.6 1.6 0 0 1-1.4-2.4z"/><path d="M12 9.4v4.6" stroke-width="1.9"/><circle cx="12" cy="18" r="1.15" fill="currentColor" stroke="none"/>',
"info": '<circle cx="12" cy="12" r="8.7" fill="currentColor" fill-opacity=".13"/><circle cx="12" cy="12" r="8.7"/><path d="M12 11v5.2" stroke-width="1.9"/><circle cx="12" cy="7.9" r="1.2" fill="currentColor" stroke="none"/>',
"check": '<circle cx="12" cy="12" r="8.7" fill="currentColor" fill-opacity=".14"/><circle cx="12" cy="12" r="8.7"/><path d="m8 12.4 2.7 2.7L16.2 9.6" stroke-width="2.1"/>',
"x": '<circle cx="12" cy="12" r="8.7" fill="currentColor" fill-opacity=".13"/><path d="m8.8 8.8 6.4 6.4M15.2 8.8l-6.4 6.4" stroke-width="2"/>',
"edit": '<path d="M4.6 19.4h3.2L19 8.2a2 2 0 0 0 0-2.8l-.4-.4a2 2 0 0 0-2.8 0L4.6 16.2z" fill="currentColor" fill-opacity=".15"/><path d="M4.6 19.4h3.2L19 8.2a2 2 0 0 0 0-2.8l-.4-.4a2 2 0 0 0-2.8 0L4.6 16.2z"/><path d="m14.4 6.6 3 3M4.6 16.2v3.2" stroke-width="1.6"/>',
"trash": '<path d="M5.6 6.6h12.8V19a1.9 1.9 0 0 1-1.9 1.9H7.5A1.9 1.9 0 0 1 5.6 19z" fill="currentColor" fill-opacity=".14"/><path d="M5.6 6.6h12.8V19a1.9 1.9 0 0 1-1.9 1.9H7.5A1.9 1.9 0 0 1 5.6 19z"/><path d="M3.6 6.6h16.8" stroke-width="1.9"/><path d="M9.4 4.1h5.2"/><path d="M9.8 10.2v7M14.2 10.2v7" stroke-width="1.5" stroke-opacity=".65"/>',
"download": '<path d="M4.4 15.4v2.8a2 2 0 0 0 2 2h11.2a2 2 0 0 0 2-2v-2.8" stroke-width="1.9"/><path d="M12 3.4v9.8" stroke-width="2"/><path d="m8.2 9.6 3.8 3.8 3.8-3.8" stroke-width="2"/><rect x="4.4" y="16.4" width="15.2" height="3.8" rx="1.4" fill="currentColor" fill-opacity=".14" stroke="none"/>',
"save": '<path d="M5.4 3.8h10L19 7.2v13a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V4.8a1 1 0 0 1 1-1z" fill="currentColor" fill-opacity=".14"/><path d="M5.4 3.8h10L19 7.2v13a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V4.8a1 1 0 0 1 1-1z"/><path d="M8.4 3.8h6.2v4.6H8.4z" fill="currentColor" fill-opacity=".34"/><rect x="8" y="13.4" width="8" height="7.8" rx="1.2" fill="currentColor" fill-opacity=".18"/><path d="M8 13.4h8v7.8H8z"/>',
"pdf": '<path d="M6.2 3.4h7.2l5.2 5.2V19a1.9 1.9 0 0 1-1.9 1.9H6.2A1.9 1.9 0 0 1 4.3 19V5.3A1.9 1.9 0 0 1 6.2 3.4z" fill="currentColor" fill-opacity=".13"/><path d="M13.4 3.4v3.8a1.4 1.4 0 0 0 1.4 1.4h3.8" fill="currentColor" fill-opacity=".34"/><path d="M6.2 3.4h7.2l5.2 5.2V19a1.9 1.9 0 0 1-1.9 1.9H6.2A1.9 1.9 0 0 1 4.3 19V5.3A1.9 1.9 0 0 1 6.2 3.4z"/><rect x="6.8" y="12.2" width="3" height="2.8" rx=".8" fill="currentColor" fill-opacity=".6" stroke="none"/><rect x="10.6" y="12.2" width="3" height="2.8" rx=".8" fill="currentColor" fill-opacity=".32" stroke="none"/><rect x="14.4" y="12.2" width="3" height="2.8" rx=".8" fill="currentColor" fill-opacity=".32" stroke="none"/><path d="M7.6 17.6h8.8" stroke-width="1.4" stroke-opacity=".5"/>',
"print": '<rect x="6.4" y="3.6" width="11.2" height="5.4" rx="1.2" fill="currentColor" fill-opacity=".2"/><rect x="3.6" y="8.6" width="16.8" height="8" rx="2" fill="currentColor" fill-opacity=".14"/><rect x="3.6" y="8.6" width="16.8" height="8" rx="2"/><rect x="6.6" y="14.4" width="10.8" height="6.4" rx="1.3" fill="#fff"/><rect x="6.6" y="14.4" width="10.8" height="6.4" rx="1.3"/><path d="M6.4 3.6h11.2v5.4" /><circle cx="17" cy="11.4" r="1" fill="currentColor" stroke="none"/>',
"eye": '<path d="M12 6.2c5.4 0 8.8 5.8 8.8 5.8s-3.4 5.8-8.8 5.8S3.2 12 3.2 12 6.6 6.2 12 6.2z" fill="currentColor" fill-opacity=".13"/><path d="M12 6.2c5.4 0 8.8 5.8 8.8 5.8s-3.4 5.8-8.8 5.8S3.2 12 3.2 12 6.6 6.2 12 6.2z"/><circle cx="12" cy="12" r="3.1" fill="currentColor" fill-opacity=".28"/><circle cx="12" cy="12" r="3.1"/>',
"refresh": '<path d="M20 12a8 8 0 0 1-13.9 5.4" stroke-width="1.9"/><path d="M4 12a8 8 0 0 1 13.9-5.4" stroke-width="1.9"/><path d="M4 7.4V12h4.6" stroke-width="1.9"/><path d="M20 16.6V12h-4.6" stroke-width="1.9"/>',
"sparkle": '<path d="M11.4 3.2 13.6 9l5.8 2.2-5.8 2.2-2.2 5.8-2.2-5.8L3.4 11.2 9.2 9z" fill="var(--accent)" fill-opacity=".22" stroke="var(--accent)" stroke-width="1.6" stroke-linejoin="round"/><path d="M18.4 15.4l.9 2.3 2.3.9-2.3.9-.9 2.3-.9-2.3-2.3-.9 2.3-.9z" fill="var(--accent)" fill-opacity=".35" stroke="var(--accent)" stroke-width="1.2"/>',
"calendar": '<rect x="3.4" y="5.4" width="17.2" height="15.2" rx="2.4" fill="currentColor" fill-opacity=".12"/><path d="M3.4 10.2h17.2" /><path d="M3.4 7.8A2.4 2.4 0 0 1 5.8 5.4h12.4a2.4 2.4 0 0 1 2.4 2.4v.6H3.4z" fill="currentColor" fill-opacity=".34" stroke="none"/><rect x="3.4" y="5.4" width="17.2" height="15.2" rx="2.4"/><path d="M7.6 3.2v3.4M16.4 3.2v3.4" stroke-width="1.9"/><rect x="7" y="13" width="3.4" height="3.2" rx="1" fill="currentColor" fill-opacity=".55" stroke="none"/><rect x="13.6" y="13" width="3.4" height="3.2" rx="1" fill="currentColor" fill-opacity=".24" stroke="none"/>',
"shield": '<path d="M12 3.2 19.6 6v6.2c0 4.6-3.2 8-7.6 9-4.4-1-7.6-4.4-7.6-9V6z" fill="currentColor" fill-opacity=".14"/><path d="M12 3.2 19.6 6v6.2c0 4.6-3.2 8-7.6 9-4.4-1-7.6-4.4-7.6-9V6z"/><path d="M12 8.4v4.2" stroke-width="1.8"/><circle cx="12" cy="15.6" r="1.1" fill="currentColor" stroke="none"/>',
"shieldCheck": '<path d="M12 3.2 19.6 6v6.2c0 4.6-3.2 8-7.6 9-4.4-1-7.6-4.4-7.6-9V6z" fill="currentColor" fill-opacity=".14"/><path d="M12 3.2 19.6 6v6.2c0 4.6-3.2 8-7.6 9-4.4-1-7.6-4.4-7.6-9V6z"/><path d="m8.6 11.8 2.4 2.4 4.4-4.6" stroke-width="2"/>',
"briefcase": '<rect x="3.4" y="7.2" width="17.2" height="12.6" rx="2.4" fill="currentColor" fill-opacity=".14"/><rect x="3.4" y="7.2" width="17.2" height="12.6" rx="2.4"/><path d="M8.6 7.2V5.6a2 2 0 0 1 2-2h2.8a2 2 0 0 1 2 2v1.6" stroke-width="1.8"/><path d="M3.4 12.2h17.2" stroke-width="1.5" stroke-opacity=".6"/><rect x="10.4" y="11" width="3.2" height="2.6" rx="1" fill="currentColor" fill-opacity=".5" stroke="none"/>',
"gauge": '<path d="M4.2 17.6a8.4 8.4 0 0 1 15.6 0z" fill="currentColor" fill-opacity=".13"/><path d="M4.2 17.6a8.4 8.4 0 0 1 15.6 0"/><path d="M7.2 16.6l.9-1.1M12 9.2v1.6M16.8 16.6l-.9-1.1" stroke-width="1.4" stroke-opacity=".7"/><path d="M12 17.6l3.8-4.6" stroke="var(--accent)" stroke-width="2"/><circle cx="12" cy="17.6" r="1.6" fill="currentColor" stroke="none"/><path d="M3 20.2h18" stroke-width="1.5" stroke-opacity=".45"/>',
"fuel": '<path d="M5 20.4V5.4a2 2 0 0 1 2-2h5.4a2 2 0 0 1 2 2v15z" fill="currentColor" fill-opacity=".14"/><path d="M5 20.4V5.4a2 2 0 0 1 2-2h5.4a2 2 0 0 1 2 2v15"/><path d="M3.4 20.4h12.8" stroke-width="1.9"/><rect x="7.2" y="6.6" width="5" height="4.4" rx="1.2" fill="currentColor" fill-opacity=".34"/><path d="M14.4 8.4h2.4a2 2 0 0 1 2 2v4.6a1.6 1.6 0 0 1-3.2 0v-3.4" stroke-width="1.7"/>',
"clock": '<circle cx="12" cy="12" r="8.7" fill="currentColor" fill-opacity=".13"/><circle cx="12" cy="12" r="8.7"/><path d="M12 5.4v1.5M12 17.1v1.5M5.4 12h1.5M17.1 12h1.5" stroke-width="1.4" stroke-opacity=".6"/><path d="M12 7.8V12l3.2 2" stroke-width="1.9"/>',
"arrowUp": '<circle cx="12" cy="12" r="8.7" fill="currentColor" fill-opacity=".12"/><path d="M12 17.4V7.2" stroke-width="2"/><path d="m7.8 11.2 4.2-4 4.2 4" stroke-width="2"/>',
"arrowDown": '<circle cx="12" cy="12" r="8.7" fill="currentColor" fill-opacity=".12"/><path d="M12 6.6v10.2" stroke-width="2"/><path d="m7.8 12.8 4.2 4 4.2-4" stroke-width="2"/>',
"filter": '<path d="M3.6 5.4h16.8l-6.6 7.6v6.2l-3.6-2.2v-4z" fill="currentColor" fill-opacity=".16"/><path d="M3.6 5.4h16.8l-6.6 7.6v6.2l-3.6-2.2v-4z"/>',
"user": '<circle cx="12" cy="8.4" r="3.9" fill="currentColor" fill-opacity=".24"/><circle cx="12" cy="8.4" r="3.9"/><path d="M4.8 20.2a7.2 7.2 0 0 1 14.4 0z" fill="currentColor" fill-opacity=".24"/><path d="M4.8 20.2a7.2 7.2 0 0 1 14.4 0"/>',
"arrowRight": '<path d="M4.6 12h13" stroke-width="2"/><path d="m12.4 6.8 5.2 5.2-5.2 5.2" stroke-width="2"/>',
"building": '<path d="M4.6 20.4V4.8a1.6 1.6 0 0 1 1.6-1.6h7.6a1.6 1.6 0 0 1 1.6 1.6v15.6z" fill="currentColor" fill-opacity=".14"/><path d="M4.6 20.4V4.8a1.6 1.6 0 0 1 1.6-1.6h7.6a1.6 1.6 0 0 1 1.6 1.6v15.6"/><path d="M15.4 20.4V9.6h2.6a1.6 1.6 0 0 1 1.6 1.6v9.2" /><path d="M2.8 20.4h18.4" stroke-width="1.9"/><rect x="7.2" y="6.4" width="2.6" height="2.6" rx=".7" fill="currentColor" fill-opacity=".5" stroke="none"/><rect x="11.4" y="6.4" width="2" height="2.6" rx=".7" fill="currentColor" fill-opacity=".3" stroke="none"/><rect x="7.2" y="11.2" width="2.6" height="2.6" rx=".7" fill="currentColor" fill-opacity=".3" stroke="none"/><rect x="11.4" y="11.2" width="2" height="2.6" rx=".7" fill="currentColor" fill-opacity=".3" stroke="none"/>',
"logout": '<path d="M10.4 4.2H6.6a2.2 2.2 0 0 0-2.2 2.2v11.2a2.2 2.2 0 0 0 2.2 2.2h3.8" stroke-width="1.9"/><path d="M14.4 8.4 18.8 12l-4.4 3.6" stroke-width="1.9"/><path d="M9.6 12h9" stroke-width="1.9"/>',
"lock": '<rect x="4.6" y="10.2" width="14.8" height="10.2" rx="2.4" fill="currentColor" fill-opacity=".15"/><rect x="4.6" y="10.2" width="14.8" height="10.2" rx="2.4"/><path d="M8 10.2V7.8a4 4 0 0 1 8 0v2.4" stroke-width="1.9"/><circle cx="12" cy="15" r="1.4" fill="currentColor" stroke="none"/><path d="M12 16.2v1.8" stroke-width="1.6"/>',
"key": '<circle cx="8" cy="15.6" r="4.2" fill="currentColor" fill-opacity=".16"/><circle cx="8" cy="15.6" r="4.2"/><circle cx="8" cy="15.6" r="1.4" fill="currentColor" stroke="none"/><path d="m11.2 12.6 7.4-7.4M16.4 7.4l2.2 2.2M14.2 9.6l1.8 1.8" stroke-width="1.8"/>',
"eyeOff": '<path d="M4 4.4 20 20.4" stroke-width="1.9"/><path d="M9.4 9.6a3.1 3.1 0 0 0 4.3 4.4" stroke-width="1.7"/><path d="M6.6 6.8A15.6 15.6 0 0 0 3.2 12s3.4 5.8 8.8 5.8c1.7 0 3.2-.6 4.5-1.4M15.2 7.4A10 10 0 0 1 20.8 12a17 17 0 0 1-2.4 3.2" stroke-width="1.7"/>',
"minus": '<path d="M5.6 12h12.8" stroke-width="2"/>',
"chevRight": '<path d="m9.4 6.6 5.4 5.4-5.4 5.4" stroke-width="2.1"/>',
"userCog": '<circle cx="9.4" cy="8.2" r="3.6" fill="currentColor" fill-opacity=".22"/><circle cx="9.4" cy="8.2" r="3.6"/><path d="M2.8 20a6.6 6.6 0 0 1 11.2-4.6" stroke-width="1.8"/><circle cx="17.6" cy="17.4" r="3" fill="currentColor" fill-opacity=".18"/><circle cx="17.6" cy="17.4" r="3"/><path d="M17.6 14v.9M17.6 19.9v.9M14.2 17.4h.9M20.1 17.4h.9" stroke-width="1.3"/>',
}

p = 'src/part3_core.js.html'
s = open(p, encoding='utf-8').read()
start = s.index('const ICONS = {')
end = s.index('\n};', start) + 3
body = 'const ICONS = {\n' + ',\n'.join(f"{k}: '{v}'".replace('\\', '\\\\') for k, v in ICONS.items()) + '\n};\n'
s = s[:start] + body + s[end:]
open(p, 'w', encoding='utf-8').write(s)
print(f"✓ {len(ICONS)} symboles redessinés en duotone « objet réel »")

# ---------------------------------------------------- pastilles plus profondes
p1 = 'src/part1_head.html'
h = open(p1, encoding='utf-8').read()

h = h.replace(""".kpi .ic-wrap{
  width:34px;height:34px;border-radius:11px;display:grid;place-items:center;flex:0 0 34px;
  background:var(--primary-50);color:var(--secondary);border:1px solid var(--primary-100);
}
.kpi .ic-wrap .ic{width:17px;height:17px}""",
""".kpi .ic-wrap{
  width:42px;height:42px;border-radius:14px;display:grid;place-items:center;flex:0 0 42px;
  background:linear-gradient(155deg,#FFFFFF 8%, var(--primary-50) 100%);
  color:var(--secondary);border:1px solid var(--primary-100);
  box-shadow:0 1px 2px rgba(74,42,99,.08), 0 4px 10px -6px rgba(74,42,99,.22), inset 0 1px 0 #fff;
}
.kpi .ic-wrap .ic{width:22px;height:22px;stroke-width:1.5}""")

h = h.replace(""".kpi.gold .ic-wrap{background:var(--accent-50);color:#9A7A15;border-color:#F0E3BC}
.kpi.ok .ic-wrap{background:var(--ok-bg);color:var(--ok);border-color:#D5EFE4}
.kpi.warn .ic-wrap{background:var(--warn-bg);color:var(--warn);border-color:#F5E7BE}""",
""".kpi.gold .ic-wrap{background:linear-gradient(155deg,#FFFFFF 8%, var(--accent-50) 100%);color:#9A7A15;border-color:#EFE0B4;
  box-shadow:0 1px 2px rgba(154,122,21,.10), 0 4px 10px -6px rgba(154,122,21,.30), inset 0 1px 0 #fff}
.kpi.ok .ic-wrap{background:linear-gradient(155deg,#FFFFFF 8%, var(--ok-bg) 100%);color:var(--ok);border-color:#D5EFE4;
  box-shadow:0 1px 2px rgba(42,134,99,.10), 0 4px 10px -6px rgba(42,134,99,.26), inset 0 1px 0 #fff}
.kpi.warn .ic-wrap{background:linear-gradient(155deg,#FFFFFF 8%, var(--warn-bg) 100%);color:var(--warn);border-color:#F0DFB4;
  box-shadow:0 1px 2px rgba(176,138,34,.10), 0 4px 10px -6px rgba(176,138,34,.26), inset 0 1px 0 #fff}""")

h = h.replace(""".card-h .ic-chip{
  width:32px;height:32px;border-radius:10px;display:grid;place-items:center;flex:0 0 32px;
  background:var(--primary-50);color:var(--secondary);border:1px solid var(--primary-100);
}
.card-h .ic-chip .ic{width:16px;height:16px}""",
""".card-h .ic-chip{
  width:38px;height:38px;border-radius:13px;display:grid;place-items:center;flex:0 0 38px;
  background:linear-gradient(155deg,#FFFFFF 8%, var(--primary-50) 100%);
  color:var(--secondary);border:1px solid var(--primary-100);
  box-shadow:0 1px 2px rgba(74,42,99,.07), 0 4px 10px -7px rgba(74,42,99,.24), inset 0 1px 0 #fff;
}
.card-h .ic-chip .ic{width:20px;height:20px;stroke-width:1.5}""")

h = h.replace(".stat-tile .ic-wrap{width:36px;height:36px;border-radius:11px;display:grid;place-items:center;flex:0 0 36px;background:var(--primary-50);color:var(--secondary);border:1px solid var(--primary-100)}",
              ".stat-tile .ic-wrap{width:40px;height:40px;border-radius:13px;display:grid;place-items:center;flex:0 0 40px;background:linear-gradient(155deg,#FFFFFF 8%, var(--primary-50) 100%);color:var(--secondary);border:1px solid var(--primary-100);box-shadow:0 1px 2px rgba(74,42,99,.07),0 4px 10px -7px rgba(74,42,99,.24),inset 0 1px 0 #fff}")
h = h.replace(".stat-tile .ic-wrap .ic{width:17px;height:17px}", ".stat-tile .ic-wrap .ic{width:21px;height:21px;stroke-width:1.5}")
h = h.replace(".quick-item .ic-wrap{width:34px;height:34px;border-radius:11px;display:grid;place-items:center;flex:0 0 34px;background:var(--surface-3);color:var(--primary)}",
              ".quick-item .ic-wrap{width:40px;height:40px;border-radius:13px;display:grid;place-items:center;flex:0 0 40px;background:linear-gradient(155deg,#FFFFFF 8%, var(--surface-3) 100%);color:var(--primary);border:1px solid var(--line-2);box-shadow:0 1px 2px rgba(74,42,99,.07),0 4px 10px -7px rgba(74,42,99,.24),inset 0 1px 0 #fff}")
h = h.replace(".quick-item .ic-wrap .ic{width:16px;height:16px}", ".quick-item .ic-wrap .ic{width:21px;height:21px;stroke-width:1.5}")
open(p1, 'w', encoding='utf-8').write(h)
print("✓ pastilles d'icônes approfondies (KPI, titres de cartes, tuiles)")
