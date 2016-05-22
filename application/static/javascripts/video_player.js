var locationHash;
var video_idx;
var videoPlaying;
var videoSource;
var playlist;

function changeVideo(event, playing, video_num) {
    if (typeof(video_num) == "number") {
        video_idx = video_num;
    }

    if (video_idx < playlist['sequence'].length && video_idx > 0) {
        window.history.replaceState({}, '', playlist['slug'] + '#' + video_idx.toString());
    } else {
        window.history.replaceState({}, '', playlist['slug']);
        video_idx = 0;
    }

    videoSource.setAttribute('src', playlist['sequence'][video_idx]['url']);

    if (playlist['sequence'][video_idx]['url'] !== 'NOSUB') {
        videoPlaying.addEventListener("loadedmetadata", function() {
            for (var i = 1; i < videoPlaying.children.length; ++i) {
                videoPlaying.removeChild(videoPlaying.children[i]);
            }
            track = document.createElement("track");
            track.kind = "captions";
            track.label = "Português";
            track.srclang = "pt";
            track.src = "/static/subtitles/" + playlist['sequence'][video_idx-1]['sub'];
            track.addEventListener("load", function() {
                this.mode = "showing";
                videoPlaying.textTracks[0].mode = "showing"; // thanks Firefox
            });
            this.appendChild(track);
            if (Math.abs(screen.height - window.innerHeight) >= 10) {
                this.setAttribute('height', this.clientHeight);
            }

        });
    }

    videoPlaying.load();
    if (playing) {
        $('.videoParte.partePlaying').removeClass('partePlaying');
        $(`.parte-${video_idx}`).addClass('partePlaying');
        videoPlaying.play();
    }
    video_idx += 1;
    if (video_idx == playlist.length) {
        video_idx = 0;
    }
}

startVideos = function(videoId, pl) {
    playlist = pl;
    locationHash = window.location.hash.substring(1);
    video_idx = 0;

    if (locationHash != "") {
        video_idx = Number(locationHash);
    }

    $(`.parte-${video_idx}`).addClass('partePlaying');

    videoPlaying = document.getElementById(videoId);
    videoSource = videoPlaying.children[0];

    if (changeUrl)
        window.history.replaceState({}, '', playlist['slug']);

    videoPlaying.addEventListener('ended', changeVideoEv, false);

    function changeVideoEv(event) {
        changeVideo(event, true);
    }

    changeVideo(undefined, false);

}
