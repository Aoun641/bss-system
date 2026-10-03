// Extremely fast, lightweight browser fingerprinter
async function getDeviceFingerprint() {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 200;
    canvas.height = 50;

    // Draw unique text shapes
    ctx.textBaseline = "top";
    ctx.font = "14px 'Arial'";
    ctx.textBaseline = "alphabetic";
    ctx.fillStyle = "#f60";
    ctx.fillRect(125,1,62,20);
    ctx.fillStyle = "#069";
    ctx.fillText("BSS v2.0 - M.ALI Schools", 2, 15);
    ctx.fillStyle = "rgba(102, 204, 0, 0.7)";
    ctx.fillText("BSS v2.0 - M.ALI Schools", 4, 17);

    const canvasData = canvas.toDataURL();
    
    return {
        browser: navigator.userAgent,
        os: navigator.platform,
        screen: `${window.screen.width}x${window.screen.height}`,
        canvas: canvasData
    };
}