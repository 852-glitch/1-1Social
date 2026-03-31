/**
 * 1:1Social Post Composer
 * Converts structured post data into branded social media posts
 * Brand: The Financial Architect
 */

class PostComposer {
  constructor(brandTokens) {
    this.brand = brandTokens;
  }

  /**
   * Main compose function
   * @param {Object} postData - Structured post content
   * @returns {string} HTML string ready for rendering or screenshot
   */
  compose(postData) {
    const {
      eyebrow,
      headline,
      headlineAccent,
      body,
      quote,
      stats
    } = postData;

    return `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Social Post - ${this.brand.brand}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="${this.brand.fonts.googleFontsUrl}" rel="stylesheet">
  ${this.generateStyles()}
</head>
<body>
  <div class="canvas">
    ${this.generateAuroraOrbs()}
    <div class="content">
      <div class="accent-line"></div>
      ${eyebrow ? `<div class="eyebrow">${eyebrow}</div>` : ''}
      ${this.generateHeadline(headline, headlineAccent)}
      <div class="divider"></div>
      ${body ? `<p class="body-text">${body}</p>` : ''}
      ${quote ? `<blockquote class="quote">${quote}</blockquote>` : ''}
      ${stats ? this.generateStats(stats) : ''}
      ${this.generateFooter()}
    </div>
  </div>
</body>
</html>
    `;
  }

  generateStyles() {
    return `
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: ${this.brand.fonts.body};
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      background: #f5f5f5;
      padding: 20px;
    }
    .canvas {
      width: ${this.brand.spacing.canvasSize};
      background: ${this.brand.colors.bgGradient};
      position: relative;
      overflow: hidden;
      box-shadow: 0 20px 60px rgba(15, 23, 42, 0.6);
    }
    .orb {
      position: absolute;
      border-radius: 50%;
      filter: blur(50px);
      opacity: 0.7;
      pointer-events: none;
      mix-blend-mode: screen;
    }
    .orb-1 {
      width: 260px; height: 260px;
      background: radial-gradient(circle at 30% 30%, rgba(67,56,202,0.5), transparent 65%);
      top: -80px; right: -60px;
    }
    .orb-2 {
      width: 220px; height: 220px;
      background: radial-gradient(circle at 30% 30%, rgba(124,58,237,0.4), transparent 70%);
      bottom: -50px; left: 10%;
    }
    .orb-3 {
      width: 180px; height: 180px;
      background: radial-gradient(circle at 40% 40%, rgba(190,24,93,0.3), transparent 70%);
      top: 35%; left: 50%;
    }
    .content { position: relative; z-index: 2; padding: ${this.brand.spacing.padding}; }
    .accent-line {
      width: ${this.brand.decorative.topAccentLine.width};
      height: ${this.brand.decorative.topAccentLine.height};
      background: ${this.brand.decorative.topAccentLine.color};
      border-radius: ${this.brand.decorative.topAccentLine.borderRadius};
      margin-bottom: 24px;
    }
    .eyebrow {
      display: inline-flex;
      align-items: center;
      padding: 4px 12px;
      border-radius: ${this.brand.spacing.eyebrowRadius};
      font-size: ${this.brand.typography.eyebrow.fontSize};
      letter-spacing: ${this.brand.typography.eyebrow.letterSpacing};
      text-transform: ${this.brand.typography.eyebrow.textTransform};
      font-weight: ${this.brand.typography.eyebrow.fontWeight};
      color: ${this.brand.colors.textSecondary};
      background: ${this.brand.colors.eyebrowBg};
      border: 1px solid ${this.brand.colors.eyebrowBorder};
      margin-bottom: 20px;
    }
    .eyebrow::before {
      content: '•';
      margin-right: 6px;
      color: ${this.brand.colors.accentTeal};
    }
    .headline {
      font-family: ${this.brand.fonts.heading};
      font-size: ${this.brand.typography.headline.fontSize};
      line-height: ${this.brand.typography.headline.lineHeight};
      letter-spacing: ${this.brand.typography.headline.letterSpacing};
      font-weight: ${this.brand.typography.headline.fontWeight};
      color: ${this.brand.colors.textPrimary};
      margin-bottom: 16px;
    }
    .headline-accent {
      color: ${this.brand.colors.accentTeal};
      font-family: ${this.brand.fonts.accent};
      font-style: ${this.brand.typography.headlineAccent.fontStyle};
    }
    .divider {
      width: 100%; height: 1px;
      background: ${this.brand.colors.divider};
      margin: 32px 0;
    }
    .body-text {
      font-size: ${this.brand.typography.body.fontSize};
      line-height: ${this.brand.typography.body.lineHeight};
      color: ${this.brand.colors.textHighlight};
      margin-bottom: 20px;
    }
    .quote {
      padding-left: 16px;
      border-left: 2px solid ${this.brand.colors.quoteBarColor};
      font-family: ${this.brand.fonts.accent};
      font-style: ${this.brand.typography.quote.fontStyle};
      font-size: ${this.brand.typography.quote.fontSize};
      line-height: 1.5;
      color: ${this.brand.colors.textSecondary};
      margin: 24px 0;
    }
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin-top: 32px;
    }
    .stat-card {
      background: ${this.brand.colors.statCardBg};
      border: 1px solid ${this.brand.colors.statCardBorder};
      border-radius: ${this.brand.spacing.statCardRadius};
      padding: 16px;
      backdrop-filter: blur(12px);
    }
    .stat-value {
      font-family: ${this.brand.fonts.heading};
      font-size: ${this.brand.typography.stat.valueFontSize};
      font-weight: ${this.brand.typography.stat.valueFontWeight};
      color: ${this.brand.colors.textPrimary};
      margin-bottom: 4px;
    }
    .stat-label {
      font-size: ${this.brand.typography.stat.labelFontSize};
      letter-spacing: ${this.brand.typography.stat.labelLetterSpacing};
      text-transform: ${this.brand.typography.stat.labelTextTransform};
      color: ${this.brand.colors.textMuted};
      font-weight: ${this.brand.typography.stat.fontWeight};
    }
    .stat-icon { font-size: 1.3rem; margin-bottom: 4px; }
    .footer {
      margin-top: 32px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .logo { display: flex; align-items: center; gap: 10px; }
    .logo-mark {
      width: 36px; height: 36px;
      background: ${this.brand.logo.bg};
      border-radius: ${this.brand.logo.borderRadius};
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: ${this.brand.fonts.heading};
      font-size: 0.9rem;
      font-weight: 700;
      color: ${this.brand.logo.text};
    }
    .brand-name {
      font-family: ${this.brand.fonts.heading};
      font-size: 0.8rem;
      font-weight: 600;
      color: ${this.brand.colors.textSecondary};
    }
    .tagline {
      font-size: ${this.brand.typography.tagline.fontSize};
      font-weight: ${this.brand.typography.tagline.fontWeight};
      letter-spacing: ${this.brand.typography.tagline.letterSpacing};
      text-transform: ${this.brand.typography.tagline.textTransform};
      color: ${this.brand.typography.tagline.color};
    }
  </style>
    `;
  }

  generateAuroraOrbs() {
    return `
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    `;
  }

  generateHeadline(headline, accentText) {
    if (!headline) return '';
    
    let html = headline;
    if (accentText) {
      html = headline.replace(accentText, `<span class="headline-accent">${accentText}</span>`);
    }
    return `<h1 class="headline">${html}</h1>`;
  }

  generateStats(stats) {
    if (!stats || stats.length === 0) return '';
    
    const statCards = stats.map(stat => `
      <div class="stat-card">
        ${stat.icon ? `<div class="stat-icon">${stat.icon}</div>` : ''}
        <div class="stat-value">${stat.value}</div>
        <div class="stat-label">${stat.label}</div>
      </div>
    `).join('');

    return `<div class="stats-grid">${statCards}</div>`;
  }

  generateFooter() {
    return `
    <div class="footer">
      <div class="logo">
        <div class="logo-mark">${this.brand.logo.initials}</div>
        <div class="brand-name">${this.brand.brand}</div>
      </div>
      <div class="tagline">${this.brand.tagline}</div>
    </div>
    `;
  }
}

// Example usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = PostComposer;
}

// Browser usage example:
// const composer = new PostComposer(brandTokens);
// const html = composer.compose({
//   eyebrow: "BEHAVIORAL FINANCE",
//   headline: "The World Cup isn't just a tournament. It's a FOMO event in disguise.",
//   headlineAccent: "FOMO event",
//   body: "Vacation rental demand in host cities is surging 200%+. Millions are asking the wrong question.",
//   quote: "Does this fit my rules — or am I just reacting to a headline?",
//   stats: [
//     { value: "200%+", label: "RENTAL DEMAND SURGE" },
//     { value: "Weeks", label: "EVENT DURATION" },
//     { icon: "∞", label: "FOMO THAT FOLLOWS" }
//   ]
// });
