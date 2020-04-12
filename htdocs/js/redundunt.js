function showRedunduntMessage() {
    let elem = document.getElementById("redundunt-message");
    elem.innerHTML = "<p class=\"rounded border p-3 mb-2 bg-info text-white text-sm-center\">省エネのため日本時間の午前1時〜7時の間、EC2インスタンスを停止しています。<br>現在、S3上でホストされた静的コンテンツのみ提供しています。</p>";
    let elemV6 = document.getElementById("love-ipv6");
    elemV6.style.display = "none";
}
