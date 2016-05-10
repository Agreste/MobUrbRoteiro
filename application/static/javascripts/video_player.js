startVideos = function(videoId, playlist) {
    var locationHash = window.location.hash.substring(1);
    var video_idx = 0;

    if (locationHash != "") {
        video_idx = Number(locationHash);
        console.log(video_idx);
    }

    var videoPlaying = document.getElementById(videoId);
    var videoSource = videoPlaying.children[0];

    if (changeUrl)
        window.history.replaceState({}, '', playlist['slug']);

    videoPlaying.addEventListener('ended', changeVideo, false);

    function changeVideo(event) {
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
            });
        }

        videoPlaying.load();
        if (typeof(event) !== 'undefined')
            videoPlaying.play();
        video_idx += 1;
        if (video_idx == playlist.length) {
            video_idx = 0;
        }
    }

    changeVideo();
}
