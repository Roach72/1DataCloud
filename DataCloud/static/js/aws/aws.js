document.addEventListener('DOMContentLoaded', function() {
    const engineSelect = document.getElementById('id_engine');
    const engineVersionSelect = document.getElementById('id_engine_version');

    const engineVersions = {
        'postgres': [
            {value: '16.3', text: '16.3'},
            {value: '15.7', text: '15.7'},
            {value: '14.12', text: '14.12'},
            {value: '13.15', text: '13.15'},
            {value: '12.19', text: '12.19'}
        ],
        'mysql': [
            {value: '8.0.33', text: '8.0.33'},
            {value: '5.7.42', text: '5.7.42'}
        ],
        'mariadb': [
            {value: '10.6.14', text: '10.6.14'},
            {value: '10.5.19', text: '10.5.19'}
        ],
        'oracle': [
            {value: '19.0.0.0.ru-2022-07.rur-2022-07.r1', text: '19.0.0.0.ru-2022-07.rur-2022-07.r1'},
            {value: '21.0.0.0.ru-2023-01.rur-2023-01.r1', text: '21.0.0.0.ru-2023-01.rur-2023-01.r1'}
        ],
        'sqlserver': [
            {value: '15.00.4236.7.v1', text: '15.00.4236.7.v1'},
            {value: '14.00.3281.6.v1', text: '14.00.3281.6.v1'}
        ],
        'redis': [
            {value: '7.0.5', text: '7.0.5'},
            {value: '6.2.6', text: '6.2.6'},
            {value: '5.0.6', text: '5.0.6'}
        ],
        'memcached': [
            {value: '1.6.12', text: '1.6.12'},
            {value: '1.5.16', text: '1.5.16'}
        ],
        'neptune': [
            {value: '1.0.4.2', text: '1.0.4.2'},
            {value: '1.0.3.0', text: '1.0.3.0'}
        ]
        // أضف هنا إصدارات المحركات الأخرى إذا لزم الأمر
    };

    engineSelect.addEventListener('change', function() {
        const selectedEngine = engineSelect.value;
        const versions = engineVersions[selectedEngine] || [];

        engineVersionSelect.innerHTML = '';
        versions.forEach(function(version) {
            const option = document.createElement('option');
            option.value = version.value;
            option.text = version.text;
            engineVersionSelect.appendChild(option);
        });
    });

    // تعبئة الخيارات لأول مرة عند تحميل الصفحة إذا كان هناك محرك محدد مسبقًا
    if (engineSelect.value) {
        const event = new Event('change');
        engineSelect.dispatchEvent(event);
    }
});
