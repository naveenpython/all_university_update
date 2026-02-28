let allNoticesData = [];

document.addEventListener('DOMContentLoaded', () => {
    fetchNotices();
    document.getElementById("searchBox").addEventListener("input", filterNotices);
});

async function fetchNotices() {
    try {
        const response = await fetch("/notices/");
        const result = await response.json();
        allNoticesData = result.data; 
        displayNotices(allNoticesData); 
    } catch (error) {
        console.error("Error fetching notices:", error);
        document.getElementById("gug-list").innerHTML = "<p class='no-result'>Server error.</p>";
        document.getElementById("mdu-list").innerHTML = "<p class='no-result'>Server error.</p>";
        document.getElementById("du-list").innerHTML = "<p class='no-result'>Server error.</p>";
    }
}

function displayNotices(noticesToDisplay) {
    const gugList = document.getElementById("gug-list");
    const mduList = document.getElementById("mdu-list");
    const duList = document.getElementById("du-list");

    gugList.innerHTML = ""; 
    mduList.innerHTML = ""; 
    duList.innerHTML = ""; 

    // ID ke hisaab se 3 hisso me baantna
    const gugNotices = noticesToDisplay.filter(notice => notice.university_id === 1);
    const mduNotices = noticesToDisplay.filter(notice => notice.university_id === 2);
    const duNotices = noticesToDisplay.filter(notice => notice.university_id === 3);

    // GUG Box
    if(gugNotices.length === 0) gugList.innerHTML = "<p class='no-result'>Koi data nahi</p>";
    else gugNotices.forEach(notice => gugList.innerHTML += createNoticeHTML(notice));

    // MDU Box
    if(mduNotices.length === 0) mduList.innerHTML = "<p class='no-result'>Koi data nahi</p>";
    else mduNotices.forEach(notice => mduList.innerHTML += createNoticeHTML(notice));

    // DU Box
    if(duNotices.length === 0) duList.innerHTML = "<p class='no-result'>Koi data nahi</p>";
    else duNotices.forEach(notice => duList.innerHTML += createNoticeHTML(notice));
}

function createNoticeHTML(notice) {
    const dateObj = new Date(notice.date_published);
    const options = { day: '2-digit', month: 'short', year: 'numeric' };
    const formattedDate = dateObj.toLocaleDateString('en-IN', options);

    return `
        <div class="notice-item">
            <a href="${notice.link}" target="_blank" class="notice-title">${notice.title}</a>
            <div class="notice-date">📅 Published on: ${formattedDate}</div>
        </div>
    `;
}

function filterNotices(event) {
    const searchInput = event.target.value.toLowerCase();
    const filteredNotices = allNoticesData.filter(notice => 
        notice.title.toLowerCase().includes(searchInput)
    );
    displayNotices(filteredNotices);
}
