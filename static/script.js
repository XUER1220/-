// 页面滚动到上传区域
function scrollToUpload() {
    document.getElementById('upload-section').scrollIntoView({ behavior: 'smooth' });
    // 等到滚动结束，添加全屏效果
    setTimeout(() => {
        document.getElementById('upload-section').classList.add('fullscreen');
    }, 500); // 延时一点点，确保滚动完成后添加全屏效果
}

// 监听滚动事件，滑动页面时显示上传区域
window.addEventListener('scroll', function () {
    let uploadSection = document.getElementById('upload-section');
    let scrollPosition = window.scrollY;

    if (scrollPosition > uploadSection.offsetTop - window.innerHeight / 1.5) {
        uploadSection.classList.add('fullscreen');
    }
});

const fileInput1 = document.getElementById('file-input1');
const previewImage1 = document.getElementById('preview-image1');
const uploadBtn1 = document.getElementById('upload-btn1');
const fileInput = document.getElementById('file-input2');
const previewVideo = document.getElementById('preview-video2');
const uploadBtn = document.getElementById('upload-btn2');
const saveBtn1 = document.getElementById('save-btn1');
const saveBtn2 = document.getElementById('save-btn2');

// 监听文件选择事件
document.getElementById('file-input1').addEventListener('change', function (event) {
    const file = event.target.files[0]; // 获取选择的文件
    if (file && file.type.startsWith('image/')) {
        // 显示图片预览
        const reader = new FileReader();
        reader.onload = function (e) {
            const previewImage = document.getElementById('preview-image1');
            previewImage.src = e.target.result;
            previewImage.style.display = 'block'; // 显示图片
            document.getElementById('upload-btn1').disabled = false; // 启用上传按钮
            document.getElementById('save-btn1').disabled = false; // 启用保存按钮
        };
        reader.readAsDataURL(file); // 读取文件内容
    } else {
        alert('请选择有效的图片文件！');
    }
});

// 监听上传按钮点击事件
document.getElementById('upload-btn1').addEventListener('click', function () {
    const file = document.getElementById('file-input1').files[0];
    if (!file) {
        alert('请先选择图片！');
        return;
    }

    // 创建 FormData 对象
    const formData = new FormData();
    formData.append('file', file); // 将文件添加到 FormData
    formData.append('type', 'image'); // 指定文件类型

    // 发送上传请求
    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('图片上传成功！');
        } else {
            alert('图片上传失败：' + data.message);
        }
    })
    .catch(error => {
        console.error('上传出错：', error);
        alert('上传出错，请稍后重试！');
    });
});

// 监听文件选择事件
fileInput.addEventListener('change', function (event) {
    const file = event.target.files[0]; // 获取选择的文件
    if (file && file.type.startsWith('video/')) {
        // 显示视频预览
        const url = URL.createObjectURL(file); // 生成临时 URL
        previewVideo.src = url;
        previewVideo.style.display = 'block';
        uploadBtn.disabled = false; // 启用上传按钮
        saveBtn2.disabled = false; // 启用保存按钮
    } else {
        alert('请选择有效的视频文件！');
    }
});

// 监听上传按钮点击事件
uploadBtn.addEventListener('click', function () {
    const file = fileInput.files[0];
    if (!file) {
        alert('请先选择视频！');
        return;
    }

    // 创建 FormData 对象
    const formData = new FormData();
    formData.append('file', file); // 将文件添加到 FormData
    formData.append('type', 'video'); // 指定文件类型

    // 发送上传请求
    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('视频上传成功！');
            saveBtn2.disabled = false; // 上传成功后启用保存按钮
        } else {
            alert('视频上传失败：' + data.message);
        }
    })
    .catch(error => {
        console.error('上传出错：', error);
        alert('上传出错，请稍后重试！');
    });
});

// 监听保存按钮点击事件
document.getElementById('save-btn1').addEventListener('click', function () {
    // 发送保存请求
    fetch('/save_image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('图片保存成功！');
        } else {
            alert('图片保存失败：' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// 监听视频保存按钮点击事件
document.getElementById('save-btn2').addEventListener('click', function () {
    // 模拟按下 'S' 键的行为
    const event = new KeyboardEvent('keydown', { key: 's' });
    document.dispatchEvent(event);
});

// 点击下滑按钮
document.querySelector('.scroll-down').addEventListener('click', scrollToUpload);