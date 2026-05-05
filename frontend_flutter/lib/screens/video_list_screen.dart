import 'package:flutter/material.dart';
import '../models/video.dart';
import '../widgets/video_card.dart';

class VideoListScreen extends StatelessWidget {
  final List<Video> videos;
  final Future<void> Function() onRefresh;
  final Function(Video) onVideoSelect;

  const VideoListScreen({
    super.key,
    required this.videos,
    required this.onRefresh,
    required this.onVideoSelect,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('My Video Requests'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: onRefresh,
          ),
        ],
      ),
      body: videos.isEmpty
          ? const Center(
              child: Text('No video requests found. Try creating one!'),
            )
          : RefreshIndicator(
              onRefresh: onRefresh,
              child: ListView.builder(
                padding: const EdgeInsets.symmetric(vertical: 8),
                itemCount: videos.length,
                itemBuilder: (context, index) {
                  final video = videos[index];
                  return VideoCard(
                    video: video,
                    onWatch: video.status == 'completed'
                        ? () => onVideoSelect(video)
                        : null,
                  );
                },
              ),
            ),
    );
  }
}
