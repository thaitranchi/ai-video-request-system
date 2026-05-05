import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';

class VideoPlayerScreen extends StatefulWidget {
  final String videoUrl;
  final String title;

  const VideoPlayerScreen({super.key, required this.videoUrl, required this.title});

  @override
  State<VideoPlayerScreen> createState() => _VideoPlayerScreenState();
}

class _VideoPlayerScreenState extends State<VideoPlayerScreen> {
  late VideoPlayerController _controller;
  bool _isError = false;

  @override
  void initState() {
    super.initState();
    _controller = VideoPlayerController.networkUrl(Uri.parse(widget.videoUrl))
      ..initialize().then((_) {
        setState(() {});
        _controller.play(); // Auto-play
      }).catchError((error) {
        setState(() {
          _isError = true;
        });
      });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: Text(widget.title),
      ),
      body: Center(
        child: _isError 
            ? const Text("Error loading video", style: TextStyle(color: Colors.white))
            : _controller.value.isInitialized
                ? AspectRatio(
                    aspectRatio: _controller.value.aspectRatio,
                    child: Stack(
                      alignment: Alignment.bottomCenter,
                      children: [
                        VideoPlayer(_controller),
                        VideoProgressIndicator(_controller, allowScrubbing: true),
                        _Controls(controller: _controller),
                      ],
                    ),
                  )
                : const CircularProgressIndicator(),
      ),
    );
  }
}

class _Controls extends StatelessWidget {
  final VideoPlayerController controller;
  const _Controls({required this.controller});

  @override
  Widget build(BuildContext context) {
    return IconButton(
      iconSize: 64,
      icon: Icon(controller.value.isPlaying ? Icons.pause : Icons.play_arrow, color: Colors.white),
      onPressed: () => controller.value.isPlaying ? controller.pause() : controller.play(),
    );
  }
}