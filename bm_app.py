import os
import csv
import datetime
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# ============================================================
# ALL DATA
# ============================================================

scrap_types = [
    {"icon": "⚙️", "name": "Iron & Steel",   "rate": "₹28 – ₹35 /kg",   "pickup": True,  "img": "/static/images/iron_steel.png"},
    {"icon": "🔌", "name": "Copper",          "rate": "₹450 – ₹500 /kg", "pickup": True,  "img": "/static/images/copper.png"},
    {"icon": "🪙", "name": "Aluminium",       "rate": "₹90 – ₹115 /kg",  "pickup": True,  "img": "/static/images/aluminium.png"},
    {"icon": "🔧", "name": "Brass",           "rate": "₹300 – ₹360 /kg", "pickup": True,  "img": "/static/images/brass.png"},
    {"icon": "🧴", "name": "PET Plastic",     "rate": "₹8 – ₹18 /kg",    "pickup": True,  "img": "/static/images/pet_plastic.png"},
    {"icon": "📰", "name": "Newspaper",       "rate": "₹12 – ₹15 /kg",   "pickup": True,  "img": "/static/images/newspaper.jpg"},
    {"icon": "📦", "name": "Cardboard",       "rate": "₹8 – ₹12 /kg",    "pickup": True,  "img": "/static/images/cardboard.jpg"},
    {"icon": "🔋", "name": "Battery",         "rate": "₹80 – ₹130 /kg",  "pickup": True,  "img": "/static/images/battery.jpg"},
    {"icon": "💻", "name": "Laptop / PC",     "rate": "₹200 – ₹800 /pc", "pickup": True,  "img": "/static/images/laptop_pc.jpg"},
    {"icon": "📱", "name": "Mobile Phone",    "rate": "₹50 – ₹200 /pc",  "pickup": True,  "img": "/static/images/mobile_phone.jpg"},
]

services = [
    {"title": "Metal Scrap Buying",      "img": "/static/images/metal_scrap.jpg", "desc": "We buy all types of ferrous and non-ferrous metals including iron, steel, copper, aluminium, brass at best market rates.",        "tag": "Free Pickup Available"},
    {"title": "Plastic Scrap Recycling", "img": "/static/images/plastic_scrap.jpg", "desc": "Collection and recycling of all plastic types - PET, HDPE, PVC, LDPE. Responsible disposal with maximum value returned.",       "tag": "Eco-Friendly Process"},
    {"title": "E-Waste Management",      "img": "/static/images/ewaste.jpg", "desc": "Safe and certified disposal of computers, laptops, mobiles, TVs, refrigerators and all electronic waste.",                      "tag": "Certified Disposal"},
    {"title": "Paper & Cardboard",       "img": "/static/images/paper_cardboard.jpg", "desc": "Buying newspapers, books, magazines, office paper, cardboard boxes at competitive prices with home pickup.",                     "tag": "Best Paper Rates"},
    {"title": "Industrial Scrap",        "img": "/static/images/industrial_scrap.jpg", "desc": "Specialized service for factories, manufacturing units — handling bulk metal, machinery, equipment and industrial waste.",        "tag": "Bulk Orders Welcome"},
    {"title": "Vehicle Scrap",           "img": "/static/images/vehicle_scrap.jpg", "desc": "Old, damaged or end-of-life vehicle disposal — cars, bikes, trucks. RTO documentation assistance provided.",                    "tag": "Document Help"},
]

why_us = [
    {"icon": "💰", "title": "Best Market Prices",   "desc": "Highest rates for your scrap — no hidden deductions, full transparency in weighing and payment."},
    {"icon": "🚚", "title": "Free Home Pickup",     "desc": "Schedule a pickup at your convenience. Our team comes to your doorstep anywhere in Bangalore — FREE."},
    {"icon": "⚡", "title": "Instant Cash Payment", "desc": "Get paid immediately on the spot — cash, UPI, bank transfer. No waiting, no delays."},
    {"icon": "🌿", "title": "Eco-Friendly",         "desc": "We ensure responsible recycling with certified processes — helping protect Bangalore's environment."},
    {"icon": "📊", "title": "Certified Weighing",   "desc": "We use government-certified digital weighing scales — complete transparency in every transaction."},
    {"icon": "🕐", "title": "Same Day Service",     "desc": "Book before noon and get same-day pickup. Quick, reliable, and punctual team always ready."},
]

testimonials = [
    {"name": "Rajesh Kumar", "area": "HSR Layout, Bangalore",             "review": "BM Enterprise gave me the best price for my old AC and refrigerator. The team was punctual, professional and paid instantly. Highly recommended!", "stars": 5, "avatar": "R"},
    {"name": "Suresh Patil", "area": "Peenya Industrial Area, Bangalore", "review": "Our factory clearance was handled perfectly. BM Enterprise arranged large vehicles and cleared all industrial scrap in one day. Excellent service!", "stars": 5, "avatar": "S"},
    {"name": "Priya Sharma", "area": "Koramangala, Bangalore",            "review": "Very honest and transparent weighing. I sold newspaper, cardboard and old iron. They paid via UPI instantly. Will definitely call again!",           "stars": 5, "avatar": "P"},
]

steps = [
    {"num": "1", "title": "Call or Book Online", "desc": "Contact us via call, WhatsApp or fill the form. Tell us what type of scrap you have."},
    {"num": "2", "title": "We Come to You",      "desc": "Our team arrives at your location at scheduled time. We weigh using certified digital scales."},
    {"num": "3", "title": "Get Paid Instantly",  "desc": "Receive immediate payment — cash or UPI — right at your doorstep. Simple and transparent!"},
]

pricing_data = [
    {"category": "Iron / MS Scrap",   "type": "Heavy Melting Scrap",     "rate": "₹28 – ₹35 /kg",   "pickup": "✅ Free"},
    {"category": "Copper",            "type": "Bare Bright / Mixed",      "rate": "₹450 – ₹500 /kg", "pickup": "✅ Free"},
    {"category": "Aluminium",         "type": "Cast / Sheet / Extrusion", "rate": "₹90 – ₹115 /kg",  "pickup": "✅ Free"},
    {"category": "Brass",             "type": "Mixed / Yellow Brass",     "rate": "₹300 – ₹360 /kg", "pickup": "✅ Free"},
    {"category": "Plastic",           "type": "PET / HDPE / Mixed",       "rate": "₹8 – ₹18 /kg",    "pickup": "✅ Free"},
    {"category": "Paper / Newspaper", "type": "Old Newspaper / Books",    "rate": "₹12 – ₹15 /kg",   "pickup": "✅ Free"},
    {"category": "Cardboard",         "type": "Corrugated Boxes",         "rate": "₹8 – ₹12 /kg",    "pickup": "✅ Free"},
    {"category": "Battery",           "type": "Lead Acid / Dry",          "rate": "₹80 – ₹130 /kg",  "pickup": "✅ Free"},
    {"category": "E-Waste",           "type": "Laptop / PC / TV",         "rate": "₹200 – ₹800 /pc", "pickup": "✅ Free"},
    {"category": "Vehicle",           "type": "Car / Bike / Truck",       "rate": "Best Quote",       "pickup": "✅ Free"},
]

contact_info = {
    "address": "BM ENTERPRISE, Address: No 87/50 , Kumbalgudu, Mysore Road, Bangalore Industrial  Area : Thagachaguppe ,  Taluk : Kumbalgodu  , District : Bangalore Urban",
    "phone1":  "+91 9900887689",
    "phone2":  "+91 7795367887",
    "email1":  "bmenterprise684@gmail.comg",
    "hours":   "Mon – Sat: 8:00 AM – 7:00 PM | Sunday: 9:00 AM – 2:00 PM",
}

# ============================================================
# HTML TEMPLATE
# ============================================================

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>BM Enterprise – #1 Scrap Dealer Bangalore | Free Home Pickup</title>
<meta name="description" content="BM Enterprise – Bangalore's most trusted scrap dealer. Best rates for iron, copper, aluminium & e-waste. FREE home pickup. Call +91 9900887689"/>
<meta name="keywords" content="scrap dealer Bangalore, kabadiwala Bangalore, iron scrap buyer, copper scrap, e-waste recycling Bangalore, free pickup"/>
<meta name="robots" content="index, follow"/>
<meta property="og:title" content="BM Enterprise – Scrap Dealer Bangalore"/>
<meta property="og:description" content="Best scrap rates in Bangalore with FREE home pickup. Call or WhatsApp now!"/>
<meta property="og:type" content="website"/>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"LocalBusiness","name":"BM Enterprise","description":"Scrap dealer and recycling company in Bangalore","telephone":"+91-9900887689","email":"bmenterprise684@gmail.com","address":{"@type":"PostalAddress","streetAddress":"No 87/50, Kumbalgudu, Mysore Road","addressLocality":"Bangalore","addressRegion":"Karnataka","addressCountry":"IN"},"openingHours":["Mo-Sa 08:00-19:00","Su 09:00-14:00"]}</script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@500;600;700&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"/>
<style>
/* ===================== RESET & ROOT ===================== */
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --ocean1:#8f745f;
  --ocean2:#a58b78;
  --ocean3:#b7a08f;
  --ocean4:#c8b8ab;
  --ocean5:#e6d8cb;
  --oceanlight:#f5ede6;
  --oceandark:#4b423d;
  --oceandeep:#3d3632;
  --white:#ffffff;
  --gray:#efefef;
  --text:#3f3834;
  --green:#5d7a66;
}
html{scroll-behavior:smooth}
body{font-family:'Inter',sans-serif;color:var(--text);background:#f6efe8;overflow-x:hidden}

/* ===================== SCROLLBAR ===================== */
::-webkit-scrollbar{width:8px}
::-webkit-scrollbar-track{background:var(--oceanlight)}
::-webkit-scrollbar-thumb{background:linear-gradient(var(--ocean1),var(--ocean3));border-radius:4px}

/* ===================== NAVBAR ===================== */
.navbar{
  position:fixed;top:0;width:100%;z-index:9999;
  background:rgba(255,255,255,0.85);
  backdrop-filter:blur(20px);
  -webkit-backdrop-filter:blur(20px);
  box-shadow:0 4px 30px rgba(31,24,20,0.15);
  padding:0 5%;display:flex;align-items:center;
  justify-content:space-between;height:70px;
  transition:all 0.3s ease;
  border-bottom:1px solid rgba(255,255,255,0.4);
}
.navbar.scrolled{background:rgba(77,66,61,0.95);box-shadow:0 4px 30px rgba(0,0,0,0.3)}
.navbar.scrolled .nav-links a{color:rgba(255,255,255,0.85)}
.navbar.scrolled .nav-links a:hover{color:var(--ocean4)}
.navbar.scrolled .logo-text{color:#fff}
.logo{display:flex;align-items:center;gap:12px;cursor:pointer}
.logo-icon{
  width:48px;height:48px;
  background:linear-gradient(135deg,var(--ocean1),var(--ocean3));
  border-radius:12px;display:flex;align-items:center;
  justify-content:center;font-size:24px;color:#fff;
  box-shadow:0 4px 15px rgba(0,153,204,0.4);
  animation:logoFloat 3s ease-in-out infinite;
}
@keyframes logoFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
.logo-text{font-size:20px;font-weight:800;color:var(--oceandark);letter-spacing:1px;transition:color 0.3s}
.logo-text span{color:var(--ocean2)}
.nav-links{display:flex;gap:28px;list-style:none}
.nav-links a{
  text-decoration:none;color:var(--text);font-weight:500;font-size:14px;
  transition:all 0.3s;position:relative;padding-bottom:4px;
}
.nav-links a::after{
  content:'';position:absolute;bottom:0;left:0;width:0;height:2px;
  background:linear-gradient(90deg,var(--ocean2),var(--ocean4));
  transition:width 0.3s ease;border-radius:2px;
}
.nav-links a:hover::after{width:100%}
.nav-links a:hover{color:var(--ocean1)}
.nav-cta{
  background:linear-gradient(135deg,var(--ocean1),var(--ocean3));
  color:#fff;border:none;padding:11px 24px;
  border-radius:25px;font-weight:700;cursor:pointer;
  font-family:'Inter',sans-serif;font-size:13px;
  box-shadow:0 4px 20px rgba(0,153,204,0.4);
  transition:all 0.3s;position:relative;overflow:hidden;
}
.nav-cta::before{
  content:'';position:absolute;top:0;left:-100%;width:100%;height:100%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.2),transparent);
  transition:left 0.5s;
}
.nav-cta:hover::before{left:100%}
.nav-cta:hover{transform:scale(1.05);box-shadow:0 6px 25px rgba(0,153,204,0.6)}

/* ===================== HERO ===================== */
.hero{
  min-height:100vh;
  background:linear-gradient(170deg,#f7efe8 0%,#f2e8df 100%);
  display:flex;align-items:center;justify-content:center;
  text-align:center;padding:120px 5% 80px;
  position:relative;overflow:hidden;
}
.hero::before{
  content:'';
  position:absolute;
  width:420px;height:420px;left:-120px;top:40px;
  background:radial-gradient(circle,rgba(143,116,95,0.14) 0%,rgba(143,116,95,0) 65%);
  pointer-events:none;
}
.hero-card{
  width:min(1100px,100%);
  background:rgba(255,255,255,0.8);
  backdrop-filter:blur(12px);
  -webkit-backdrop-filter:blur(12px);
  border-radius:26px;
  padding:46px 38px;
  box-shadow:0 15px 50px rgba(31,24,20,0.15);
  border:1px solid rgba(255,255,255,0.6);
  display:block;
  align-items:center;
  position:relative;
  z-index:2;
}
.hero-kicker{
  font-size:13px;
  letter-spacing:2.5px;
  text-transform:uppercase;
  color:#7f6555;
  margin-bottom:16px;
  font-weight:600;
}
.hero-copy h1{
  font-family:'Playfair Display',serif;
  font-size:clamp(2.1rem,4.8vw,4.2rem);
  color:#1f1814;
  line-height:1.06;
  margin-bottom:16px;
}
.hero-copy h1 .brand{
  color:#7c5d4b;
  background:none;
  -webkit-text-fill-color:inherit;
}
.hero-copy p{
  color:#5c4d43;
  font-size:1.02rem;
  line-height:1.8;
  max-width:700px;
  margin-left:auto;
  margin-right:auto;
  margin-bottom:28px;
}
.hero-actions{display:flex;gap:14px;flex-wrap:wrap}
.hero-actions{justify-content:center}

/* Animated Ocean Waves */
.ocean{display:none}
.wave{
  position:absolute;bottom:0;left:0;width:200%;height:100%;
  background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 120'%3E%3Cpath fill='rgba(255,255,255,0.08)' d='M0,60 C240,100 480,20 720,60 C960,100 1200,20 1440,60 L1440,120 L0,120 Z'/%3E%3C/svg%3E") repeat-x;
  background-size:50% 100%;
  animation:waveMove 8s linear infinite;
}
.wave2{
  position:absolute;bottom:0;left:0;width:200%;height:100%;
  background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 120'%3E%3Cpath fill='rgba(255,255,255,0.05)' d='M0,80 C360,20 720,100 1080,40 C1260,10 1380,70 1440,80 L1440,120 L0,120 Z'/%3E%3C/svg%3E") repeat-x;
  background-size:50% 100%;
  animation:waveMove 12s linear infinite reverse;
}
.wave3{
  position:absolute;bottom:0;left:0;width:200%;height:80%;
  background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 120'%3E%3Cpath fill='rgba(0,188,212,0.1)' d='M0,40 C180,80 360,0 540,50 C720,100 900,20 1080,60 C1260,100 1350,30 1440,50 L1440,120 L0,120 Z'/%3E%3C/svg%3E") repeat-x;
  background-size:50% 100%;
  animation:waveMove 6s linear infinite;
}
@keyframes waveMove{from{transform:translateX(0)}to{transform:translateX(-50%)}}

/* Floating Bubbles */
.bubbles{display:none}
.bubble{
  position:absolute;border-radius:50%;
  background:radial-gradient(circle at 30% 30%,rgba(255,255,255,0.3),rgba(255,255,255,0.05));
  border:1px solid rgba(255,255,255,0.15);
  animation:bubbleRise linear infinite;
}
.b1{width:20px;height:20px;left:10%;animation-duration:8s;animation-delay:0s}
.b2{width:35px;height:35px;left:25%;animation-duration:12s;animation-delay:2s}
.b3{width:15px;height:15px;left:40%;animation-duration:7s;animation-delay:4s}
.b4{width:45px;height:45px;left:55%;animation-duration:15s;animation-delay:1s}
.b5{width:25px;height:25px;left:70%;animation-duration:9s;animation-delay:3s}
.b6{width:18px;height:18px;left:85%;animation-duration:11s;animation-delay:5s}
.b7{width:30px;height:30px;left:15%;animation-duration:13s;animation-delay:6s}
.b8{width:12px;height:12px;left:90%;animation-duration:6s;animation-delay:2s}
@keyframes bubbleRise{
  0%{transform:translateY(100vh) scale(0);opacity:0}
  10%{opacity:1}
  90%{opacity:0.5}
  100%{transform:translateY(-100px) scale(1);opacity:0}
}

/* Glowing Particles */
.particles{display:none}
.particle{
  position:absolute;width:4px;height:4px;border-radius:50%;
  background:rgba(77,208,225,0.8);
  animation:particleFloat linear infinite;
  box-shadow:0 0 8px rgba(77,208,225,0.8);
}
@keyframes particleFloat{
  0%{transform:translateY(0) rotate(0deg);opacity:1}
  100%{transform:translateY(-600px) rotate(720deg);opacity:0}
}

.hero-content{position:relative;z-index:5}
.btn-primary{
  background:#2e1f17;
  color:#fff;padding:14px 28px;border-radius:10px;
  text-decoration:none;font-weight:800;font-size:15px;
  box-shadow:0 10px 28px rgba(46,31,23,0.25);transition:all 0.3s;
  border:none;cursor:pointer;font-family:'Inter',sans-serif;
  position:relative;overflow:hidden;
}
.btn-primary::after{
  content:'';position:absolute;top:50%;left:50%;
  width:0;height:0;background:rgba(0,105,148,0.15);
  border-radius:50%;transform:translate(-50%,-50%);
  transition:width 0.6s,height 0.6s;
}
.btn-primary:hover::after{width:300px;height:300px}
.btn-primary:hover{transform:translateY(-4px);box-shadow:0 15px 40px rgba(0,0,0,0.35)}
.btn-secondary{
  background:#fff;color:#2e1f17;padding:14px 28px;border-radius:10px;
  text-decoration:none;font-weight:700;font-size:15px;
  border:1px solid #d7c7bb;transition:all 0.3s;
  backdrop-filter:blur(5px);position:relative;overflow:hidden;
}
.btn-secondary:hover{
  background:#f8f1ec;
  border-color:#c7b0a2;transform:translateY(-4px);
  box-shadow:0 10px 30px rgba(46,31,23,0.18);
}

/* Stats Counter */
.hero-stats{display:flex;gap:20px;justify-content:center;flex-wrap:wrap}
.stat-box{
  background:rgba(255,255,255,0.6);
  backdrop-filter:blur(10px);
  -webkit-backdrop-filter:blur(10px);
  padding:18px 22px;border-radius:14px;text-align:center;
  border:1px solid rgba(255,255,255,0.5);
  box-shadow:0 4px 15px rgba(31,24,20,0.1);
  transition:all 0.3s;cursor:default;
}
.stat-box:hover{background:rgba(255,255,255,0.8);transform:translateY(-5px);box-shadow:0 8px 25px rgba(31,24,20,0.15)}
.stat-box h3{
  font-size:2rem;font-weight:800;color:#2e1f17;
}
.stat-box p{font-size:12px;color:#7a6659;font-weight:500;margin-top:4px}

/* ===================== TICKER ===================== */
.ticker{
  background:#e9ddd1;
  color:#4b423d;padding:14px 0;overflow:hidden;
  position:relative;z-index:10;
  box-shadow:0 3px 12px rgba(60,48,38,0.1);
}
.ticker::before,.ticker::after{
  content:'';position:absolute;top:0;width:100px;height:100%;z-index:1;
}
.ticker::before{left:0;background:linear-gradient(90deg,#e9ddd1,transparent)}
.ticker::after{right:0;background:linear-gradient(-90deg,#e9ddd1,transparent)}
.ticker-inner{display:flex;animation:ticker 28s linear infinite;white-space:nowrap}
.ticker-inner span{
  padding:0 35px;font-size:14px;font-weight:600;
  display:flex;align-items:center;gap:8px;
}
.ticker-inner span::before{content:'•';font-size:12px}
@keyframes ticker{from{transform:translateX(0)}to{transform:translateX(-50%)}}

/* ===================== SECTIONS ===================== */
.section-pad{padding:90px 5%}
.white-bg{background:#fff}
.gray-bg{background:var(--gray)}
.ocean-bg{background:linear-gradient(135deg,#f0e5dc 0%,#eadfd4 100%);color:var(--text)}

.section-title{text-align:center;margin-bottom:55px}
.section-title h2{
  font-size:clamp(1.8rem,4vw,2.6rem);font-weight:800;color:var(--oceandark);
  position:relative;display:inline-block;
}
.section-title h2::after{
  content:'';position:absolute;bottom:-8px;left:50%;transform:translateX(-50%);
  width:0;height:4px;background:linear-gradient(90deg,var(--ocean1),var(--ocean3));
  border-radius:2px;animation:lineGrow 1s ease forwards 0.5s;
}
@keyframes lineGrow{to{width:80px}}
.section-title.light h2{color:var(--oceandark)}
.section-title p{
  color:#666;margin-top:20px;font-size:16px;
  max-width:600px;margin-left:auto;margin-right:auto;line-height:1.7;
}
.section-title.light p{color:#6a5b52}

/* ===================== GLASS MORPHISM ===================== */
.glass-effect{
  background:rgba(255,255,255,0.7);
  backdrop-filter:blur(10px);
  -webkit-backdrop-filter:blur(10px);
  border:1px solid rgba(255,255,255,0.4);
  box-shadow:0 8px 32px rgba(31,24,20,0.1);
}
.glass-effect:hover{
  background:rgba(255,255,255,0.85);
  box-shadow:0 12px 40px rgba(31,24,20,0.15);
}

/* ===================== SERVICES ===================== */
.services{background:var(--gray)}
.services-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:28px}
.service-card{
  background:rgba(255,255,255,0.7);
  backdrop-filter:blur(15px);
  -webkit-backdrop-filter:blur(15px);
  border-radius:24px;padding:38px 28px;text-align:center;
  transition:all 0.4s cubic-bezier(0.175,0.885,0.32,1.275);
  box-shadow:0 8px 32px rgba(31,24,20,0.12);
  border:1.5px solid rgba(255,255,255,0.5);
  position:relative;overflow:hidden;
  display:flex;flex-direction:column;align-items:center;
}
.service-card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:4px;
  background:linear-gradient(90deg,var(--ocean1),var(--ocean3),var(--ocean4));
  transform:scaleX(0);transition:transform 0.4s ease;
}
.service-card:hover::before{transform:scaleX(1)}
.service-card:hover{
  transform:translateY(-12px);
  background:rgba(255,255,255,0.85);
  box-shadow:0 20px 50px rgba(0,105,148,0.2);
  border-color:rgba(255,255,255,0.7);
}
.service-card-img{
  width:100%;height:200px;object-fit:cover;
  border-radius:16px;margin-bottom:22px;
  transition:transform 0.5s ease;
  box-shadow:0 4px 15px rgba(31,24,20,0.15);
}
.service-card:hover .service-card-img{
  transform:scale(1.08);
  box-shadow:0 8px 25px rgba(0,153,204,0.2);
}
.service-card h3{font-size:1.15rem;font-weight:700;color:var(--oceandark);margin-bottom:12px}
.service-card p{font-size:14px;color:#555;line-height:1.7}
.service-tag{
  display:inline-block;
  background:linear-gradient(135deg,var(--oceanlight),var(--ocean5));
  color:var(--ocean1);padding:5px 14px;border-radius:12px;
  font-size:11px;font-weight:700;margin-top:14px;
  border:1px solid var(--ocean5);
}

/* ===================== SCRAP TYPES ===================== */
.types-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:24px}
.type-card{
  border-radius:20px;padding:0;text-align:center;
  background:rgba(255,255,255,0.7);
  backdrop-filter:blur(12px);
  -webkit-backdrop-filter:blur(12px);
  border:1px solid rgba(255,255,255,0.5);transition:all 0.4s;
  position:relative;overflow:hidden;cursor:default;
  box-shadow:0 8px 20px rgba(60,48,38,0.12);
}
.type-card:hover{
  transform:translateY(-8px) scale(1.02);
  background:rgba(255,255,255,0.85);
  box-shadow:0 15px 45px rgba(0,105,148,0.18);
  border-color:rgba(255,255,255,0.7);
}
.type-card-img{
  width:100%;height:160px;object-fit:cover;
  display:block;border-radius:20px 20px 0 0;
  transition:transform 0.5s ease;
  background:linear-gradient(135deg,rgba(143,116,95,0.1),rgba(183,160,143,0.1));
}
.type-card:hover .type-card-img{transform:scale(1.08)}
.type-card-body{padding:16px 14px 18px}
.type-card h3{font-size:15px;font-weight:700;color:var(--oceandark);margin-bottom:6px}
.type-card .price{
  color:var(--green);font-weight:800;font-size:13px;
  background:rgba(0,137,123,0.1);padding:3px 10px;border-radius:8px;
  display:inline-block;
}
.pickup-badge{
  display:block;background:rgba(0,137,123,0.12);color:var(--green);
  padding:4px 10px;border-radius:8px;font-size:11px;font-weight:600;margin-top:8px;
}

/* ===================== WHY CHOOSE ===================== */
.why-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:28px}
.why-card{
  background:rgba(255,255,255,0.7);
  backdrop-filter:blur(12px);
  -webkit-backdrop-filter:blur(12px);
  border:1px solid rgba(255,255,255,0.5);border-radius:24px;
  padding:35px 22px;text-align:center;transition:all 0.4s;
  position:relative;overflow:hidden;
  box-shadow:0 8px 20px rgba(60,48,38,0.12);
}
.why-card::before{
  content:'';position:absolute;inset:0;border-radius:24px;
  background:linear-gradient(135deg,rgba(255,255,255,0.15),transparent);
  opacity:0;transition:opacity 0.4s;
}
.why-card:hover::before{opacity:1}
.why-card:hover{
  background:rgba(255,255,255,0.85);
  transform:translateY(-8px);
  box-shadow:0 15px 40px rgba(60,48,38,0.15);
  border-color:rgba(255,255,255,0.7);
}
.why-card .icon{font-size:48px;margin-bottom:18px;display:block;transition:transform 0.4s;background:linear-gradient(135deg,var(--oceanlight),var(--ocean5));width:80px;height:80px;margin-left:auto;margin-right:auto;border-radius:16px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 15px rgba(0,153,204,0.15)}
.why-card:hover .icon{transform:scale(1.2) rotate(5deg);box-shadow:0 8px 25px rgba(0,153,204,0.25)}
.why-card h3{font-size:1.1rem;font-weight:700;margin-bottom:10px;color:var(--oceandark)}
.why-card p{font-size:13px;opacity:1;line-height:1.7;color:#6a5b52}

/* ===================== HOW IT WORKS ===================== */
.how{background:var(--gray)}
.steps{display:flex;justify-content:center;flex-wrap:wrap;gap:10px;position:relative;align-items:center}
.steps::before{
  content:'';position:absolute;top:42px;left:20%;right:20%;height:3px;
  background:linear-gradient(90deg,var(--ocean1),var(--ocean3),var(--ocean4));
  border-radius:2px;z-index:0;
}
.step{text-align:center;padding:35px 25px;flex:1;min-width:200px;position:relative;z-index:1}
.step-num{
  width:65px;height:65px;margin:0 auto 18px;
  background:linear-gradient(135deg,var(--ocean1),var(--ocean3));
  border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-size:24px;font-weight:800;color:#fff;
  box-shadow:0 8px 30px rgba(0,153,204,0.5);
  border:4px solid #fff;transition:all 0.4s;
  position:relative;z-index:2;
}
.step:hover .step-num{
  transform:scale(1.2);
  box-shadow:0 12px 40px rgba(0,153,204,0.7);
  background:linear-gradient(135deg,var(--oceandark),var(--ocean1));
}
.step h3{font-size:1rem;font-weight:700;color:var(--oceandark);margin-bottom:10px}
.step p{font-size:13px;color:#555;line-height:1.6}

.table-wrap{overflow-x:auto;border-radius:20px;box-shadow:0 10px 40px rgba(31,24,20,0.15)}
.pricing-table{width:100%;border-collapse:collapse;border-radius:20px;overflow:hidden}
.pricing-table th{
  background:linear-gradient(135deg,var(--ocean1),var(--ocean2));
  color:#fff;padding:20px 22px;text-align:left;font-size:14px;font-weight:700;
  backdrop-filter:blur(5px);
}
.pricing-table tr:nth-child(even){background:rgba(255,255,255,0.5)}
.pricing-table tr:nth-child(odd){background:rgba(255,255,255,0.7)}
.pricing-table td{padding:16px 22px;font-size:14px;border-bottom:1px solid rgba(0,188,212,0.1);transition:all 0.2s}
.pricing-table tr:hover td{background:rgba(0,188,212,0.1);padding-left:28px}
.pricing-table .price-val{color:var(--green);font-weight:800;font-size:15px}

/* ===================== TESTIMONIALS ===================== */
.testimonials{background:linear-gradient(135deg,var(--oceanlight),#b2ebf2)}
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:28px}
.review-card{
  background:rgba(255,255,255,0.8);
  backdrop-filter:blur(15px);
  -webkit-backdrop-filter:blur(15px);
  border-radius:24px;padding:32px;
  box-shadow:0 8px 32px rgba(31,24,20,0.15);
  transition:all 0.4s;
  position:relative;overflow:hidden;
  border:1px solid rgba(255,255,255,0.6);
}
.review-card::before{
  content:'"';position:absolute;top:-10px;right:20px;
  font-size:120px;color:rgba(0,188,212,0.08);font-family:Georgia,serif;
  line-height:1;pointer-events:none;
}
.review-card:hover{
  transform:translateY(-8px);
  background:rgba(255,255,255,0.95);
  box-shadow:0 16px 50px rgba(0,105,148,0.2);
}
.stars{font-size:18px;margin-bottom:14px;letter-spacing:2px}
.review-card>p{font-size:14px;color:#444;line-height:1.8;font-style:italic}
.reviewer{display:flex;align-items:center;gap:14px;margin-top:20px}
.reviewer-avatar{
  width:50px;height:50px;border-radius:50%;
  background:linear-gradient(135deg,var(--ocean1),var(--ocean3));
  display:flex;align-items:center;justify-content:center;
  color:#fff;font-weight:800;font-size:20px;
  box-shadow:0 4px 15px rgba(0,153,204,0.4);flex-shrink:0;
}
.reviewer-info h4{font-size:15px;font-weight:700;color:var(--oceandark)}
.reviewer-info p{font-size:12px;color:#888}

/* ===================== CONTACT ===================== */
.contact{background:#fff}
.contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:55px;align-items:start}
.contact-info h3{font-size:1.6rem;font-weight:800;color:var(--oceandark);margin-bottom:28px}
.contact-item{display:flex;gap:16px;margin-bottom:24px;align-items:flex-start}
.contact-item-icon{
  width:50px;height:50px;min-width:50px;
  background:rgba(255,255,255,0.6);
  backdrop-filter:blur(8px);
  -webkit-backdrop-filter:blur(8px);
  border-radius:14px;display:flex;align-items:center;justify-content:center;
  font-size:20px;color:var(--ocean1);
  box-shadow:0 4px 15px rgba(0,153,204,0.15);
  transition:all 0.3s;
  border:1px solid rgba(255,255,255,0.4);
}
.contact-item:hover .contact-item-icon{
  background:linear-gradient(135deg,var(--ocean1),var(--ocean3));
  color:#fff;transform:scale(1.1);
  box-shadow:0 8px 25px rgba(0,153,204,0.3);
  border-color:transparent;
}
.contact-item-text h4{font-size:14px;font-weight:700;color:var(--oceandark)}
.contact-item-text p{font-size:13px;color:#666;line-height:1.7}
.contact-form{
  background:rgba(255,255,255,0.7);
  backdrop-filter:blur(15px);
  -webkit-backdrop-filter:blur(15px);
  border-radius:24px;padding:38px;
  box-shadow:0 8px 32px rgba(31,24,20,0.15);
  border:1px solid rgba(255,255,255,0.6);
}
.contact-form h3{font-size:1.5rem;font-weight:800;color:var(--oceandark);margin-bottom:28px}
.form-group{margin-bottom:20px}
.form-group label{display:block;font-size:13px;font-weight:700;color:var(--oceandark);margin-bottom:7px}
.form-group input,.form-group select,.form-group textarea{
  width:100%;padding:13px 16px;
  border:2px solid rgba(0,188,212,0.3);
  background:rgba(255,255,255,0.8);
  backdrop-filter:blur(5px);
  -webkit-backdrop-filter:blur(5px);
  border-radius:12px;font-family:'Inter',sans-serif;font-size:13px;
  color:var(--text);transition:all 0.3s;outline:none;
}
.form-group input:focus,.form-group select:focus,.form-group textarea:focus{
  border-color:var(--ocean3);
  box-shadow:0 0 0 4px rgba(0,188,212,0.1);
  transform:translateY(-1px);
}
.form-group textarea{height:110px;resize:vertical}
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.submit-btn{
  width:100%;background:linear-gradient(135deg,var(--ocean1),var(--ocean3));
  color:#fff;border:none;padding:16px;border-radius:14px;
  font-weight:800;font-size:15px;cursor:pointer;
  font-family:'Inter',sans-serif;transition:all 0.3s;
  box-shadow:0 6px 25px rgba(0,153,204,0.4);
  position:relative;overflow:hidden;
}
.submit-btn::before{
  content:'';position:absolute;top:0;left:-100%;width:100%;height:100%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.2),transparent);
  transition:left 0.5s;
}
.submit-btn:hover::before{left:100%}
.submit-btn:hover{transform:translateY(-3px);box-shadow:0 10px 35px rgba(0,153,204,0.6)}
.form-msg{padding:13px 16px;border-radius:12px;font-size:14px;font-weight:600;margin-bottom:16px}
.form-msg.success{background:#e0f2f1;color:#00695c;border:1px solid #80cbc4}
.form-msg.error{background:#fce4ec;color:#c62828;border:1px solid #f48fb1}
.hidden{display:none}

/* ===================== MAP ===================== */
.map-section{padding:0 5% 90px}
.map-container{border-radius:24px;overflow:hidden;box-shadow:0 15px 50px rgba(0,105,148,0.25);border:3px solid var(--ocean5)}
.map-container iframe{width:100%;height:380px;border:none;display:block}

/* ===================== FOOTER ===================== */
footer{
  background:linear-gradient(135deg,#3f3834 0%,#4a413c 50%,#5a4f48 100%);
  color:#fff;padding:70px 5% 30px;position:relative;overflow:hidden;
}
footer::before{
  content:'';position:absolute;top:0;left:0;right:0;height:4px;
  background:linear-gradient(90deg,var(--ocean1),var(--ocean3),var(--ocean4),var(--ocean3),var(--ocean1));
  background-size:200% auto;animation:footerLine 3s linear infinite;
}
@keyframes footerLine{0%{background-position:0% center}100%{background-position:200% center}}
.footer-grid{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:45px;margin-bottom:45px}
.footer-brand p{font-size:13px;opacity:0.7;line-height:1.9;margin:16px 0}
.footer-social{display:flex;gap:12px}
.social-icon{
  width:40px;height:40px;border-radius:10px;
  background:rgba(0,188,212,0.15);border:1px solid rgba(0,188,212,0.3);
  display:flex;align-items:center;justify-content:center;
  font-size:16px;cursor:pointer;transition:all 0.3s;
  text-decoration:none;color:#fff;
}
.social-icon:hover{
  background:linear-gradient(135deg,var(--ocean1),var(--ocean3));
  transform:translateY(-3px);box-shadow:0 6px 20px rgba(0,153,204,0.4);
  border-color:transparent;
}
.footer-col h4{font-size:15px;font-weight:700;margin-bottom:20px;color:var(--ocean4)}
.footer-col ul{list-style:none}
.footer-col ul li{margin-bottom:12px}
.footer-col ul li a{
  color:rgba(255,255,255,0.65);text-decoration:none;font-size:13px;
  transition:all 0.3s;display:flex;align-items:center;gap:8px;
}
.footer-col ul li a:hover{color:var(--ocean4);padding-left:5px}
.footer-col ul li a i{color:var(--ocean4);font-size:11px;transition:transform 0.3s}
.footer-col ul li a:hover i{transform:translateX(3px)}
.footer-bottom{
  border-top:1px solid rgba(255,255,255,0.08);
  padding-top:28px;text-align:center;font-size:13px;opacity:0.65;
}
.footer-bottom span{color:var(--ocean4)}
.footer-bottom a{color:var(--ocean4);text-decoration:none}
.mb-15{margin-bottom:15px}

/* ===================== FLOATING BUTTONS ===================== */
.float-btn{
  position:fixed;bottom:30px;right:30px;z-index:9998;
  background:linear-gradient(135deg,#25d366,#128c7e);
  color:#fff;width:58px;height:58px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:28px;text-decoration:none;
  box-shadow:0 6px 25px rgba(37,211,102,0.5);
  animation:waPulse 2s infinite;
}
@keyframes waPulse{
  0%,100%{transform:scale(1);box-shadow:0 6px 25px rgba(37,211,102,0.5)}
  50%{transform:scale(1.1);box-shadow:0 8px 35px rgba(37,211,102,0.8)}
}
.scroll-top{
  position:fixed;bottom:178px;right:32px;z-index:9998;
  background:linear-gradient(135deg,var(--ocean1),var(--ocean3));
  color:#fff;width:44px;height:44px;border-radius:50%;
  display:none;align-items:center;justify-content:center;
  font-size:17px;cursor:pointer;
  box-shadow:0 4px 20px rgba(0,153,204,0.5);
  transition:all 0.3s;border:none;
}
.scroll-top:hover{transform:translateY(-3px);box-shadow:0 8px 30px rgba(0,153,204,0.7)}

/* ===================== ANIMATIONS ===================== */
.fade-up{opacity:0;transform:translateY(40px);transition:all 0.7s cubic-bezier(0.16,1,0.3,1)}
.fade-up.visible{opacity:1;transform:translateY(0)}
.fade-left{opacity:0;transform:translateX(-40px);transition:all 0.7s cubic-bezier(0.16,1,0.3,1)}
.fade-left.visible{opacity:1;transform:translateX(0)}
.fade-right{opacity:0;transform:translateX(40px);transition:all 0.7s cubic-bezier(0.16,1,0.3,1)}
.fade-right.visible{opacity:1;transform:translateX(0)}
.zoom-in{opacity:0;transform:scale(0.8);transition:all 0.6s cubic-bezier(0.16,1,0.3,1)}
.zoom-in.visible{opacity:1;transform:scale(1)}

/* Staggered delay */
.d1{transition-delay:0.1s}.d2{transition-delay:0.2s}
.d3{transition-delay:0.3s}.d4{transition-delay:0.4s}
.d5{transition-delay:0.5s}.d6{transition-delay:0.6s}

/* ===================== RESPONSIVE ===================== */
@media(max-width:1024px){
  .footer-grid{grid-template-columns:1fr 1fr}
  .steps::before{display:none}
}
@media(max-width:768px){
  .nav-links{display:none}
  .contact-grid{grid-template-columns:1fr}
  .form-row{grid-template-columns:1fr}
  .hero-card{grid-template-columns:1fr;padding:20px}
  .hero-media{min-height:280px}
}
@media(max-width:600px){
  .footer-grid{grid-template-columns:1fr}
  .hero-stats{gap:12px}
  .stat-box{padding:14px 18px}
}

/* ===================== HAMBURGER MENU ===================== */
.hamburger{display:none;flex-direction:column;gap:5px;cursor:pointer;padding:8px;border:none;background:transparent}
.hamburger span{display:block;width:24px;height:2.5px;background:var(--oceandark);border-radius:2px;transition:all 0.35s}
.hamburger.open span:nth-child(1){transform:translateY(7.5px) rotate(45deg)}
.hamburger.open span:nth-child(2){opacity:0;transform:scaleX(0)}
.hamburger.open span:nth-child(3){transform:translateY(-7.5px) rotate(-45deg)}
.navbar.scrolled .hamburger span{background:#fff}
@media(max-width:768px){
  .hamburger{display:flex}
  .nav-links{
    display:none;position:fixed;top:70px;left:0;right:0;
    background:rgba(255,255,255,0.98);backdrop-filter:blur(20px);
    flex-direction:column;gap:0;padding:10px 0;
    box-shadow:0 12px 40px rgba(0,0,0,0.15);
    border-top:1px solid #eee;z-index:9990;
  }
  .nav-links.open{display:flex}
  .nav-links li a{padding:15px 30px;font-size:15px;border-bottom:1px solid #f5f5f5;display:block}
  .nav-cta{display:none}
}
/* ===================== CALL FLOAT BUTTON ===================== */
.call-btn{
  position:fixed;bottom:100px;right:30px;z-index:9998;
  background:linear-gradient(135deg,#0088cc,#005fa3);
  color:#fff;width:58px;height:58px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:22px;text-decoration:none;
  box-shadow:0 6px 25px rgba(0,136,204,0.5);transition:all 0.3s;
}
.call-btn:hover{transform:scale(1.12);box-shadow:0 8px 35px rgba(0,136,204,0.8)}
</style>
</head>
<body>

<!-- FLOATING BUTTONS -->
<a href="https://wa.me/917795367887" class="float-btn" target="_blank" title="Chat on WhatsApp">
  <i class="fab fa-whatsapp"></i>
</a>
<a href="tel:+919900887689" class="call-btn" title="Call Us Now">
  <i class="fas fa-phone"></i>
</a>
<button class="scroll-top" id="scrollTop">
  <i class="fas fa-chevron-up"></i>
</button>

<!-- ===================== NAVBAR ===================== -->
<nav class="navbar" id="navbar">
  <div class="logo" onclick="window.scrollTo({top:0,behavior:'smooth'})">
    <div class="logo-text">BM <span>ENTERPRISE</span></div>
  </div>
  <ul class="nav-links">
    <li><a href="#home">Home</a></li>
    <li><a href="#services">Services</a></li>
    <li><a href="#types">Scrap Types</a></li>
    <li><a href="#pricing">Pricing</a></li>
    <li><a href="#about">About</a></li>
    <li><a href="#contact">Contact</a></li>
  </ul>
  <button class="nav-cta" onclick="document.getElementById('contact').scrollIntoView({behavior:'smooth'})">
    📞 Get Free Quote
  </button>
  <button class="hamburger" id="hamburger" aria-label="Toggle Navigation">
    <span></span><span></span><span></span>
  </button>
</nav>

<!-- ===================== HERO ===================== -->
<section class="hero" id="home">
  <div class="hero-card">
    <div class="hero-content hero-copy">
      <div class="hero-kicker">BM ENTERPRISE</div>
      <h1>We help businesses and homes recycle smarter with <span class="brand">trusted scrap services</span>.</h1>
      <p>Professional scrap collection in Bangalore with transparent rates, accurate weighing, and dependable doorstep pickup for households, offices, and industries.</p>
      <div class="hero-actions">
        <a href="#contact" class="btn-primary">Get a Free Quote</a>
        <a href="tel:+917795367887" class="btn-secondary">Book Pickup</a>
      </div>
      <div class="hero-stats">
      <div class="stat-box zoom-in d1">
        <h3 data-count="10">0</h3><p>Years Experience</p>
      </div>
      <div class="stat-box zoom-in d2">
        <h3 data-count="5000">0</h3><p>Happy Customers</p>
      </div>
      <div class="stat-box zoom-in d3">
        <h3 data-count="50">0</h3><p>Areas Covered</p>
      </div>
      <div class="stat-box zoom-in d4">
        <h3 data-count="100">0</h3><p>Eco-Friendly %</p>
      </div>
      </div>
    </div>
  </div>
</section>

<!-- ===================== TICKER ===================== -->
<div class="ticker">
  <div class="ticker-inner">
    {% set items = ["Metal Scrap","Plastic Scrap","E-Waste","Paper Scrap","Industrial Scrap","Vehicle Scrap","Battery Scrap","Cardboard","Copper Wire","Aluminium","Brass","Iron & Steel"] %}
    {% for item in items %}<span>{{ item }}</span>{% endfor %}
    {% for item in items %}<span>{{ item }}</span>{% endfor %}
  </div>
</div>

<!-- ===================== SERVICES ===================== -->
<section class="services section-pad" id="services">
  <div class="section-title">
    <h2>Our Services</h2>
    <p>Comprehensive scrap management services across Bangalore with complete transparency and best market rates.</p>
  </div>
  <div class="services-grid">
    {% for s in services %}
    <div class="service-card fade-up d{{ loop.index }}">
      <img class="service-card-img" src="{{ s.img }}" alt="{{ s.title }}" loading="lazy"
           onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
      <div class="service-icon" style="display:none;align-items:center;justify-content:center;font-size:32px;background:linear-gradient(135deg,var(--oceanlight),var(--ocean5))"><i class="fas fa-check"></i></div>
      <h3>{{ s.title }}</h3>
      <p>{{ s.desc }}</p>
      <span class="service-tag">{{ s.tag }}</span>
    </div>
    {% endfor %}
  </div>
</section>

<!-- ===================== SCRAP TYPES ===================== -->
<section class="section-pad white-bg" id="types">
  <div class="section-title">
    <h2>Types of Scrap We Accept</h2>
    <p>From household to industrial — we accept all types of scrap across Bangalore.</p>
  </div>
  <div class="types-grid">
    {% for t in scrap_types %}
    <div class="type-card zoom-in d{{ loop.index if loop.index <= 6 else loop.index - 6 }}">
      <img class="type-card-img" src="{{ t.img }}" alt="{{ t.name }} scrap" loading="lazy"
           onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
      <div class="type-card-img" style="display:none;align-items:center;justify-content:center;font-size:48px;background:linear-gradient(135deg,var(--oceanlight),#b2ebf2)">{{ t.icon }}</div>
      <div class="type-card-body">
        <h3>{{ t.name }}</h3>
        <p class="price">{{ t.rate }}</p>
        {% if t.pickup %}<span class="pickup-badge">✅ Free Pickup</span>{% endif %}
      </div>
    </div>
    {% endfor %}
  </div>
</section>

<!-- ===================== WHY CHOOSE US ===================== -->
<section class="ocean-bg section-pad" id="about">
  <div class="section-title light">
    <h2>Why Choose BM Enterprise?</h2>
    <p>Trusted by thousands of households and businesses across Bangalore.</p>
  </div>
  <div class="why-grid">
    {% for w in why_us %}
    <div class="why-card fade-up d{{ loop.index }}">
      <div class="icon"><i class="fas fa-check"></i></div>
      <h3>{{ w.title }}</h3>
      <p>{{ w.desc }}</p>
    </div>
    {% endfor %}
  </div>
</section>

<!-- ===================== HOW IT WORKS ===================== -->
<section class="how section-pad">
  <div class="section-title">
    <h2>How It Works</h2>
    <p>Sell your scrap in just 3 simple steps — quick, easy, hassle-free!</p>
  </div>
  <div class="steps">
    {% for step in steps %}
    <div class="step fade-up d{{ loop.index }}">
      <div class="step-num">{{ step.num }}</div>
      <h3>{{ step.title }}</h3>
      <p>{{ step.desc }}</p>
    </div>
    {% endfor %}
  </div>
</section>

<!-- ===================== PRICING ===================== -->
<section class="section-pad gray-bg" id="pricing">
  <div class="section-title">
    <h2>Current Scrap Rates - Bangalore</h2>
    <p>*Rates are approximate and subject to market fluctuations. Call us for exact current rates.</p>
  </div>
  <div class="table-wrap fade-up">
    <table class="pricing-table">
      <thead>
        <tr>
          <th>Scrap Category</th>
          <th>Type / Grade</th>
          <th>Our Rate</th>
          <th>Pickup</th>
        </tr>
      </thead>
      <tbody>
        {% for row in pricing_data %}
        <tr>
          <td>{{ row.category }}</td>
          <td>{{ row.type }}</td>
          <td class="price-val">{{ row.rate }}</td>
          <td>{{ row.pickup }}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</section>

<!-- ===================== TESTIMONIALS ===================== -->
<section class="testimonials section-pad">
  <div class="section-title">
    <h2>What Our Customers Say</h2>
    <p>Thousands of satisfied customers across Bangalore trust BM Enterprise.</p>
  </div>
  <div class="reviews-grid">
    {% for t in testimonials %}
    <div class="review-card fade-up d{{ loop.index }}">
      <div class="stars">{% for i in range(t.stars) %}⭐{% endfor %}</div>
      <p>"{{ t.review }}"</p>
      <div class="reviewer">
        <div class="reviewer-avatar">{{ t.avatar }}</div>
        <div class="reviewer-info">
          <h4>{{ t.name }}</h4>
          <p>{{ t.area }}</p>
        </div>
      </div>
    </div>
    {% endfor %}
  </div>
</section>

<!-- ===================== CONTACT ===================== -->
<section class="contact section-pad" id="contact">
  <div class="section-title">
    <h2>Contact Us</h2>
    <p>Get in touch for free pickup booking, scrap valuation or any inquiry. We serve all areas of Bangalore!</p>
  </div>
  <div class="contact-grid">
    <div class="contact-info fade-left">
      <h3>Get In Touch</h3>
      <div class="contact-item">
        <div class="contact-item-icon"><i class="fas fa-map-marker-alt"></i></div>
        <div class="contact-item-text">
          <h4>Our Address</h4>
          <p>{{ contact_info.address }}</p>
        </div>
      </div>
      <div class="contact-item">
        <div class="contact-item-icon"><i class="fas fa-phone-alt"></i></div>
        <div class="contact-item-text">
          <h4>Phone / WhatsApp</h4>
          <p>{{ contact_info.phone1 }}<br/>{{ contact_info.phone2 }}</p>
        </div>
      </div>
      <div class="contact-item">
        <div class="contact-item-icon"><i class="fas fa-envelope"></i></div>
        <div class="contact-item-text">
          <h4>Email Us</h4>
          <p>{{ contact_info.email1 }}<br/>{{ contact_info.email2 }}</p>
        </div>
      </div>
      <div class="contact-item">
        <div class="contact-item-icon"><i class="fas fa-clock"></i></div>
        <div class="contact-item-text">
          <h4>Working Hours</h4>
          <p>{{ contact_info.hours }}</p>
        </div>
      </div>
    </div>
    <div class="contact-form fade-right">
      <h3>Book Free Pickup</h3>
      <div id="form-msg" class="form-msg hidden"></div>
      <form id="pickupForm">
        <div class="form-row">
          <div class="form-group">
            <label>Your Name *</label>
            <input type="text" id="fname" placeholder="Enter your name" required/>
          </div>
          <div class="form-group">
            <label>Phone Number *</label>
            <input type="tel" id="phone" placeholder="+91 XXXXX XXXXX" required/>
          </div>
        </div>
        <div class="form-group">
          <label>Your Area / Location *</label>
          <input type="text" id="area" placeholder="e.g. Koramangala, Whitefield..." required/>
        </div>
        <div class="form-group">
          <label>Type of Scrap</label>
          <select id="scrap_type">
            <option value="">-- Select Scrap Type --</option>
            <option>Metal / Iron / Steel</option>
            <option>Copper / Aluminium / Brass</option>
            <option>Plastic Scrap</option>
            <option>Paper / Cardboard</option>
            <option>E-Waste (Electronics)</option>
            <option>Vehicle Scrap</option>
            <option>Battery</option>
            <option>Industrial / Bulk Scrap</option>
            <option>Mixed / Multiple Types</option>
          </select>
        </div>
        <div class="form-group">
          <label>Additional Message</label>
          <textarea id="message" placeholder="Tell us about scrap quantity, preferred pickup time, etc."></textarea>
        </div>
        <button type="submit" class="submit-btn" id="submitBtn">Book Free Pickup Now</button>
      </form>
    </div>
  </div>
</section>

<!-- MAP -->
<div class="map-section">
  <div class="map-container fade-up">
    <iframe
      src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d497811.1000787054!2d77.35073034179688!3d12.95428674241565!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bae1670c9b44e6d%3A0xf8dfc3e8517e4fe0!2sBengaluru%2C%20Karnataka!5e0!3m2!1sen!2sin!4v1700000000000"
      allowfullscreen="" loading="lazy">
    </iframe>
  </div>
</div>

<!-- ===================== FOOTER ===================== -->
<footer>
  <div class="footer-grid">
    <div class="footer-brand">
      <div class="logo mb-15">
        <div class="logo-text" style="color:#fff">BM <span>ENTERPRISE</span></div>
      </div>
      <p>Bangalore's most trusted scrap dealer and recycling company. We buy all types of scrap at the best prices with free home pickup across all of Bangalore.</p>
      <div class="footer-social">
        <a class="social-icon" href="#" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
        <a class="social-icon" href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
        <a class="social-icon" href="https://wa.me/917795367887" aria-label="WhatsApp"><i class="fab fa-whatsapp"></i></a>
        <a class="social-icon" href="#" aria-label="YouTube"><i class="fab fa-youtube"></i></a>
      </div>
    </div>
    <div class="footer-col">
      <h4>Quick Links</h4>
      <ul>
        <li><a href="#home"><i class="fas fa-chevron-right"></i>Home</a></li>
        <li><a href="#services"><i class="fas fa-chevron-right"></i>Services</a></li>
        <li><a href="#types"><i class="fas fa-chevron-right"></i>Scrap Types</a></li>
        <li><a href="#pricing"><i class="fas fa-chevron-right"></i>Pricing</a></li>
        <li><a href="#contact"><i class="fas fa-chevron-right"></i>Contact</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Our Services</h4>
      <ul>
        {% for s in services %}
        <li><a href="#services"><i class="fas fa-chevron-right"></i>{{ s.title }}</a></li>
        {% endfor %}
      </ul>
    </div>
    <div class="footer-col">
      <h4>Contact Info</h4>
      <ul>
        <li><a href="#"><i class="fas fa-map-marker-alt"></i>Bangalore, Karnataka</a></li>
        <li><a href="tel:+917795367887"><i class="fas fa-phone"></i>{{ contact_info.phone1 }}</a></li>
        <li><a href="mailto:info@bmenterprise.in"><i class="fas fa-envelope"></i>{{ contact_info.email1 }}</a></li>
        <li><a href="#"><i class="fas fa-clock"></i>Mon–Sat: 8AM–7PM</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <p>© 2025 <span>BM Enterprise</span>. All Rights Reserved. | Built with 🐍 Python & Flask 🌊 |
      <a href="#">Privacy Policy</a> | <a href="#">Terms of Service</a>
    </p>
  </div>
</footer>

<!-- ===================== JAVASCRIPT ===================== -->
<script>
// ---- Hamburger Menu Toggle ----
const hamburger = document.getElementById('hamburger');
const navMenu   = document.querySelector('.nav-links');
if(hamburger && navMenu){
  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('open');
    navMenu.classList.toggle('open');
  });
  navMenu.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      hamburger.classList.remove('open');
      navMenu.classList.remove('open');
    });
  });
}

// ---- Generate Particles ----
(function(){
  const container = document.getElementById('particles');
  if(!container) return;
  for(let i = 0; i < 25; i++){
    const p = document.createElement('div');
    p.className = 'particle';
    p.style.cssText = `
      left:${Math.random()*100}%;
      bottom:${Math.random()*30}%;
      width:${Math.random()*5+2}px;
      height:${Math.random()*5+2}px;
      animation-duration:${Math.random()*8+5}s;
      animation-delay:${Math.random()*6}s;
      opacity:${Math.random()*0.7+0.3};
    `;
    container.appendChild(p);
  }
})();

// ---- Counter Animation ----
function animateCounter(el, target, suffix=''){
  let start = 0;
  const dur = 2000;
  const step = target / (dur / 16);
  const timer = setInterval(() => {
    start += step;
    if(start >= target){
      el.textContent = target.toLocaleString() + suffix;
      clearInterval(timer);
    } else {
      el.textContent = Math.floor(start).toLocaleString() + suffix;
    }
  }, 16);
}

// ---- Navbar scroll effect ----
const navbar = document.getElementById('navbar');
const scrollBtn = document.getElementById('scrollTop');
let countersDone = false;

window.addEventListener('scroll', () => {
  if(window.scrollY > 80){
    navbar.classList.add('scrolled');
    scrollBtn.style.display = 'flex';
  } else {
    navbar.classList.remove('scrolled');
    scrollBtn.style.display = 'none';
  }
});

// ---- Scroll Top ----
scrollBtn.addEventListener('click', () => window.scrollTo({top:0,behavior:'smooth'}));

// ---- Smooth scroll for anchor links ----
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', function(e){
    e.preventDefault();
    const t = document.querySelector(this.getAttribute('href'));
    if(t) t.scrollIntoView({behavior:'smooth'});
  });
});

// ---- Intersection Observer for animations ----
const animEls = document.querySelectorAll('.fade-up, .fade-left, .fade-right, .zoom-in');
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if(entry.isIntersecting){
      entry.target.classList.add('visible');
      // Trigger counters when hero stats appear
      if(!countersDone && entry.target.closest('.hero-stats')){
        countersDone = true;
        document.querySelectorAll('[data-count]').forEach(el => {
          const val = parseInt(el.getAttribute('data-count'));
          const suffix = val === 100 ? '%' : val >= 1000 ? '+' : '+';
          animateCounter(el, val, suffix);
        });
      }
    }
  });
}, {threshold:0.15});
animEls.forEach(el => observer.observe(el));

// ---- Start counters on load if already visible ----
window.addEventListener('load', () => {
  const statsSection = document.querySelector('.hero-stats');
  if(statsSection){
    const rect = statsSection.getBoundingClientRect();
    if(rect.top < window.innerHeight && !countersDone){
      countersDone = true;
      document.querySelectorAll('[data-count]').forEach(el => {
        const val = parseInt(el.getAttribute('data-count'));
        const suffix = val === 100 ? '%' : '+';
        animateCounter(el, val, suffix);
      });
    }
  }
});

// ---- Form Submit → Flask API ----
document.getElementById('pickupForm').addEventListener('submit', async function(e){
  e.preventDefault();
  const btn    = document.getElementById('submitBtn');
  const msgBox = document.getElementById('form-msg');

  btn.innerHTML = '⏳ Submitting...';
  btn.disabled = true;

  const payload = {
    name:       document.getElementById('fname').value,
    phone:      document.getElementById('phone').value,
    area:       document.getElementById('area').value,
    scrap_type: document.getElementById('scrap_type').value,
    message:    document.getElementById('message').value,
  };

  try {
    const res    = await fetch('/book-pickup', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify(payload)
    });
    const result = await res.json();
    msgBox.className = 'form-msg success';
    msgBox.innerHTML = result.message +
      ' <strong>Redirecting you to WhatsApp... 📲</strong>';
    msgBox.classList.remove('hidden');
    this.reset();
    // Open WhatsApp with booking details
    if(result.whatsapp_url){
      setTimeout(() => { window.open(result.whatsapp_url, '_blank'); }, 800);
    }
  } catch(err){
    msgBox.className = 'form-msg error';
    msgBox.classList.remove('hidden');
    msgBox.textContent = '❌ Something went wrong. Please call us directly!';
  }
  btn.innerHTML = 'Book Free Pickup Now';
  btn.disabled = false;
});
</script>
</body>
</html>
"""

# ============================================================
# FLASK ROUTES
# ============================================================

@app.route("/")
def home():
    return render_template_string(
        HTML,
        scrap_types  = scrap_types,
        services     = services,
        why_us       = why_us,
        testimonials = testimonials,
        steps        = steps,
        pricing_data = pricing_data,
        contact_info = contact_info,
    )

@app.route("/book-pickup", methods=["POST"])
def book_pickup():
    data = request.get_json() or {}

    # ---- Server-side validation ----
    name       = (data.get('name') or '').strip()
    phone      = (data.get('phone') or '').strip()
    area       = (data.get('area') or '').strip()
    scrap_type = (data.get('scrap_type') or '').strip()
    message    = (data.get('message') or '').strip()

    if not name or not phone or not area:
        return jsonify({"success": False, "message": "❌ Name, phone and area are required."}), 400
    if len(phone) < 10:
        return jsonify({"success": False, "message": "❌ Please enter a valid phone number."}), 400

    # ---- Log to console ----
    print("\n" + "🌊"*20)
    print("  📬  NEW PICKUP BOOKING RECEIVED!")
    print("🌊"*20)
    print(f"  👤 Name       : {name}")
    print(f"  📞 Phone      : {phone}")
    print(f"  📍 Area       : {area}")
    print(f"  ♻️  Scrap Type : {scrap_type}")
    print(f"  💬 Message    : {message}")
    print("🌊"*20 + "\n")

    # ---- Save booking to CSV (skipped on read-only filesystems like Vercel) ----
    try:
        csv_file   = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bookings.csv')
        file_exists = os.path.isfile(csv_file)
        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['timestamp','name','phone','area','scrap_type','message'])
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'name': name, 'phone': phone, 'area': area,
                'scrap_type': scrap_type, 'message': message
            })
    except Exception:
        pass  # Vercel read-only filesystem — bookings still go via WhatsApp redirect

    # ---- Build WhatsApp message & URL ----
    wa_text = (
        f"🚚 *New Pickup Booking – BM Enterprise*\n\n"
        f"👤 *Name:* {name}\n"
        f"📞 *Phone:* {phone}\n"
        f"📍 *Area:* {area}\n"
        f"♻️ *Scrap Type:* {scrap_type or 'Not specified'}\n"
        f"💬 *Message:* {message or 'None'}\n\n"
        f"🕐 *Booked on:* {datetime.datetime.now().strftime('%d %b %Y, %I:%M %p')}"
    )
    import urllib.parse
    wa_number  = "917795367887"          # WhatsApp business number (with country code, no +)
    wa_url     = f"https://wa.me/{wa_number}?text={urllib.parse.quote(wa_text)}"

    print(f"  📲 WhatsApp URL : {wa_url}\n")

    return jsonify({
        "success": True,
        "message": f"✅ Thank you {name}! Your pickup is booked. We'll call you within 30 minutes. 🚚",
        "whatsapp_url": wa_url
    })

@app.route("/api/scrap-rates")
def scrap_rates():
    return jsonify({"status":"success","data":scrap_types})

@app.route("/api/services")
def get_services():
    return jsonify({"status":"success","data":services})

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    print("\n" + "="*40)
    print("  BM ENTERPRISE WEBSITE IS RUNNING!")
    print("  Open => http://localhost:5000")
    print("="*40 + "\n")
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)