function drawBarChart(canvasId, data, color='#00e5ff') {
    const cv = document.getElementById(canvasId);
    if (!cv || !data || data.length === 0) return;
    const ctx = cv.getContext('2d');
    const w = cv.width = cv.offsetWidth; const h = cv.height = 220;
    const max = Math.max(...data.map(d => d.total), 1);
    const bw = (w - 40) / data.length - 8;
    
    data.forEach((d, i) => {
        const bh = (d.present / max) * (h - 50);
        const x = 20 + i * (bw + 8); const y = h - 30 - bh;
        const grad = ctx.createLinearGradient(0, y, 0, y + bh);
        grad.addColorStop(0, color); grad.addColorStop(1, 'rgba(0,229,255,0.1)');
        ctx.fillStyle = grad; ctx.beginPath(); ctx.roundRect(x, y, bw, bh, [4, 4, 0, 0]); ctx.fill();
        
        ctx.fillStyle = '#94a3b8'; ctx.font = '10px Inter'; ctx.textAlign = 'center';
        ctx.fillText(d.name.replace('Class ','C'), x + bw/2, h - 10);
        ctx.fillStyle = '#fff'; ctx.font = 'bold 11px Inter'; ctx.fillText(d.present, x + bw/2, y - 8);
    });
}

function drawLineChart(canvasId, data, color='#c084fc') {
    const cv = document.getElementById(canvasId);
    if (!cv || !data || data.length === 0) return;
    const ctx = cv.getContext('2d');
    const w = cv.width = cv.offsetWidth; const h = cv.height = 220;
    const max = Math.max(...data.map(d => d.count), 1);
    const stepX = (w - 40) / (data.length - 1 || 1);
    
    ctx.strokeStyle = color; ctx.lineWidth = 3; ctx.lineJoin = 'round';
    ctx.shadowColor = color; ctx.shadowBlur = 10;
    ctx.beginPath();
    data.forEach((d, i) => {
        const x = 20 + i * stepX; const y = h - 40 - (d.count / max) * (h - 70);
        if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    });
    ctx.stroke(); ctx.shadowBlur = 0;
    
    data.forEach((d, i) => {
        const x = 20 + i * stepX; const y = h - 40 - (d.count / max) * (h - 70);
        ctx.fillStyle = '#0f172a'; ctx.beginPath(); ctx.arc(x, y, 5, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = color; ctx.beginPath(); ctx.arc(x, y, 3, 0, Math.PI * 2); ctx.fill();
        
        ctx.fillStyle = '#94a3b8'; ctx.font = '10px Inter'; ctx.textAlign = 'center';
        ctx.fillText(d.date.slice(5), x, h - 15);
        ctx.fillStyle = '#fff'; ctx.font = 'bold 11px Inter'; ctx.fillText(d.count, x, y - 12);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    try { drawBarChart('classChart', JSON.parse(document.getElementById('class-data').textContent || '[]')); } catch(e) {}
    try { drawLineChart('trendChart', JSON.parse(document.getElementById('trend-data').textContent || '[]')); } catch(e) {}
});