function showRedundantMessage() {
    let elem = document.getElementById("redundunt-message");
    elem.innerHTML = "<p class=\"rounded border p-3 mb-2 bg-info text-white text-sm-center\">経費削減のため現在EC2インスタンスを停止しており、S3上で静的コンテンツのみ提供しています。</p>";
    let elemV6 = document.getElementById("love-ipv6");
    elemV6.style.display = "none";
}
