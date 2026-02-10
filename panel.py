<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>우리 스틸 원가 마스터</title>
    <style>
        :root { --gold: #D4AF37; --bg: #121212; --card: #1E1E1E; --accent: #FF4D4D; }
        body { background: var(--bg); color: #E0E0E0; font-family: 'Pretendard', sans-serif; margin: 0; padding: 20px; }
        .app-container { max-width: 450px; margin: 0 auto; background: var(--card); border-radius: 20px; padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.7); border: 1px solid #333; }
        h2 { color: var(--gold); text-align: center; letter-spacing: 2px; margin-bottom: 30px; }
        
        .section-title { font-size: 0.8em; color: var(--gold); margin-bottom: 10px; font-weight: bold; }
        .input-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px; }
        .input-box { background: #2A2A2A; padding: 10px; border-radius: 10px; }
        label { display: block; font-size: 0.75em; color: #888; margin-bottom: 5px; }
        input, select { width: 100%; background: none; border: none; color: white; font-size: 1.1em; outline: none; box-sizing: border-box; }
        
        /* 홀덤 스타일 버튼 */
        .toggle-group { display: flex; gap: 5px; margin-bottom: 15px; }
        .toggle-btn { flex: 1; padding: 10px; background: #333; border: 1px solid #444; color: #888; border-radius: 8px; cursor: pointer; font-size: 0.9em; }
        .toggle-btn.active { background: var(--gold); color: black; font-weight: bold; border-color: var(--gold); }

        .result-area { margin-top: 25px; padding: 20px; background: #000; border-radius: 15px; border-left: 5px solid var(--gold); }
        .result-label { font-size: 0.9em; color: #888; }
        .result-price { font-size: 2.5em; font-weight: bold; color: var(--gold); margin: 5px 0; }
        
        button.calc-btn { width: 100%; padding: 18px; background: var(--gold); border: none; border-radius: 12px; font-weight: bold; font-size: 1.2em; margin-top: 10px; cursor: pointer; transition: 0.2s; }
        button.calc-btn:active { transform: scale(0.98); opacity: 0.9; }
    </style>
</head>
<body>

<div class="app-container">
    <h2>COST SOLVER</h2>

    <div class="section-title">BASE PRICE (매입단가)</div>
    <div class="input-row">
        <div class="input-box"><label>코일 (kg)</label><input type="number" id="coilPrice" value="1100"></div>
        <div class="input-box"><label>가공비 (고정)</label><input type="number" id="processFee" value="2700"></div>
    </div>

    <div class="section-title">MATERIAL (심재 선택)</div>
    <div class="toggle-group" id="coreGroup">
        <button class="toggle-btn active" onclick="setCore('EPS')">EPS</button>
        <button class="toggle-btn" onclick="setCore('GW')">그라스울</button>
        <button class="toggle-btn" onclick="setCore('URE')">우레탄</button>
    </div>

    <div id="gwDensityArea" style="display:none;">
        <div class="section-title">GW DENSITY (밀도)</div>
        <div class="toggle-group">
            <button class="toggle-btn active" id="btn48k" onclick="setDensity(48, 1770)">48K</button>
            <button class="toggle-btn" id="btn64k" onclick="setDensity(64, 1600)">64K</button>
        </div>
    </div>

    <div class="input-row">
        <div class="input-box"><label id="coreLabel">EPS 50T 보드값</label><input type="number" id="corePrice" value="3650"></div>
        <div class="input-box"><label>두께 (T)</label><input type="number" id="thickness" value="150"></div>
    </div>

    <div class="section-title">COIL TYPE (조합)</div>
    <select id="coilWeight" class="input-box" style="width:100%; border:1px solid #444;">
        <option value="8.867">내부(1040) / 외부(1219)</option>
        <option value="8.164">내부(1040) / 내부(1040)</option>
    </select>

    <button class="calc-btn" onclick="calculate()">RUN CALCULATION</button>

    <div class="result-area">
        <div class="result-label">ESTIMATED PRODUCTION COST (1M)</div>
        <div class="result-price" id="finalPrice">0원</div>
    </div>
</div>

<script>
    let currentCore = 'EPS';
    let currentDensity = 48;

    function setCore(type) {
        currentCore = type;
        const btns = document.querySelectorAll('#coreGroup .toggle-btn');
        btns.forEach(b => b.classList.remove('active'));
        event.target.classList.add('active');

        const gwArea = document.getElementById('gwDensityArea');
        const coreLabel = document.getElementById('coreLabel');
        const coreInput = document.getElementById('corePrice');

        if(type === 'GW') {
            gwArea.style.display = 'block';
            coreLabel.innerText = "GW kg당 매입가";
            coreInput.value = (currentDensity === 48) ? 1770 : 1600;
        } else {
            gwArea.style.display = 'none';
            coreLabel.innerText = type === 'EPS' ? "EPS 50T 보드값" : "우레탄 m당 원액비";
            coreInput.value = type === 'EPS' ? 3650 : 18000;
        }
    }

    function setDensity(k, price) {
        currentDensity = k;
        document.getElementById('btn48k').classList.toggle('active', k === 48);
        document.getElementById('btn64k').classList.toggle('active', k === 64);
        document.getElementById('corePrice').value = price;
    }

    function calculate() {
        const coilP = parseFloat(document.getElementById('coilPrice').value);
        const coreP = parseFloat(document.getElementById('corePrice').value);
        const thick = parseFloat(document.getElementById('thickness').value);
        const coilW = parseFloat(document.getElementById('coilWeight').value);
        const procF = parseFloat(document.getElementById('processFee').value);

        let coilTotal = coilP * coilW;
        let coreTotal = 0;

        if(currentCore === 'EPS') {
            coreTotal = (thick / 50) * coreP;
        } else if(currentCore === 'GW') {
            coreTotal = (thick / 1000) * currentDensity * 1.219 * coreP;
        } else { // 우레탄
            coreTotal = (thick / 50) * coreP; 
        }

        const total = Math.round(coilTotal + coreTotal + procF);
        document.getElementById('finalPrice').innerText = total.toLocaleString() + "원";
    }
</script>
</body>
</html>