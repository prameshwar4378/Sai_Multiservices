(function($) {
    'use strict';
    
    $(document).ready(function() {
        // Find video file input
        $('input[type="file"][name*="video_file"]').each(function() {
            var $input = $(this);
            var $form = $input.closest('form');
            
            // Create progress bar container
            var progressHTML = `
                <div class="upload-progress-container" style="margin-top: 10px; display: none;">
                    <div class="upload-progress-bar" style="height: 20px; background: #f0f0f0; border-radius: 10px; overflow: hidden;">
                        <div class="upload-progress-fill" style="height: 100%; background: #79aec8; width: 0%; transition: width 0.3s ease;"></div>
                    </div>
                    <div class="upload-progress-text" style="text-align: center; font-size: 12px; margin-top: 5px;">
                        <span class="percentage">0%</span>
                        <span class="status"> - Preparing upload...</span>
                    </div>
                </div>
            `;
            
            $input.after(progressHTML);
            var $progressContainer = $input.next('.upload-progress-container');
            var $progressFill = $progressContainer.find('.upload-progress-fill');
            var $progressText = $progressContainer.find('.upload-progress-text');
            var $percentage = $progressContainer.find('.percentage');
            var $status = $progressContainer.find('.status');
            
            // Handle file selection
            $input.on('change', function() {
                var file = this.files[0];
                if (file) {
                    var fileSize = (file.size / (1024 * 1024)).toFixed(2);
                    $progressContainer.show();
                    $status.text(' - Selected: ' + file.name + ' (' + fileSize + ' MB)');
                }
            });
            
            // Intercept form submission for video uploads
            $form.on('submit', function(e) {
                var videoFile = $input[0].files[0];
                if (videoFile && videoFile.size > 10 * 1024 * 1024) { // For files > 10MB
                    e.preventDefault();
                    uploadWithProgress(videoFile, $input, $progressFill, $percentage, $status, $form);
                    return false;
                }
            });
        });
        
        function uploadWithProgress(file, $input, $progressFill, $percentage, $status, $form) {
            var formData = new FormData($form[0]);
            var xhr = new XMLHttpRequest();
            
            // Generate upload ID
            var uploadId = 'upload_' + Date.now();
            
            // Update progress
            xhr.upload.addEventListener('progress', function(e) {
                if (e.lengthComputable) {
                    var percentComplete = Math.round((e.loaded / e.total) * 100);
                    $progressFill.css('width', percentComplete + '%');
                    $percentage.text(percentComplete + '%');
                    $status.text(' - Uploading...');
                    
                    // Update admin interface with current progress
                    updateAdminProgressBar(percentComplete);
                }
            });
            
            xhr.addEventListener('load', function(e) {
                if (xhr.status === 200) {
                    $progressFill.css('width', '100%');
                    $percentage.text('100%');
                    $status.text(' - Upload complete! Processing...');
                    
                    // Submit the form normally after upload
                    setTimeout(function() {
                        $form.off('submit').submit();
                    }, 1000);
                } else {
                    $status.text(' - Upload failed. Please try again.');
                    $progressFill.css('background', '#dc3545');
                }
            });
            
            xhr.addEventListener('error', function() {
                $status.text(' - Network error. Please try again.');
                $progressFill.css('background', '#dc3545');
            });
            
            // Send the request
            xhr.open('POST', $form.attr('action'));
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            xhr.send(formData);
        }
        
        function updateAdminProgressBar(percentage) {
            // Update any global progress indicator
            $('.global-progress').remove();
            if ($('.breadcrumbs').length) {
                $('.breadcrumbs').after(`
                    <div class="global-progress" style="background: #fff; padding: 10px; margin: 10px 0; border-left: 4px solid #79aec8;">
                        <strong>Upload Progress:</strong>
                        <div style="height: 10px; background: #f0f0f0; margin: 5px 0; border-radius: 5px;">
                            <div style="height: 100%; background: #79aec8; width: ${percentage}%; border-radius: 5px;"></div>
                        </div>
                        <div style="font-size: 12px;">${percentage}% complete</div>
                    </div>
                `);
            }
        }
        
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
    });
})(django.jQuery);