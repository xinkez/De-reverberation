clear;
figure(1); clf;

load '0005_00.mat'

RGB_free = IV_free(:,:,1:3);
RGB_free = RGB_free(:);

alpha_free = IV_free(:,:,4);
alpha_free = alpha_free(:);

RGB_room = IV_room(:,:,1:3);
RGB_room = RGB_room(:);

alpha_room = IV_room(:,:,4);
alpha_room = alpha_room(:);

N_bins = 500;

subplot(2,2,1);
histogram(RGB_free, N_bins);
line(mean(RGB_free) + 2*std(RGB_free)*[1 1],[0 200000],'LineStyle','--')
line(mean(RGB_free) - 2*std(RGB_free)*[1 1],[0 200000],'LineStyle','--')
text(mean(RGB_free) - 2*std(RGB_free), 0.1*10^5, '\mu-2\sigma', 'HorizontalAlignment','right')
text(mean(RGB_free) + 2*std(RGB_free), 0.1*10^5, '\mu+2\sigma', 'HorizontalAlignment','left')
info = {['mean \mu: ' num2str(mean(RGB_free), '%.2e')], ...
        ['standard deviation \sigma: ' num2str(std(RGB_free), '%.2e')], ...
        ['max: ' num2str(max(RGB_free))], ...
        ['min: ' num2str(min(RGB_free))]};
annotation('textbox', [0.31 0.9 0 0], 'String', info, 'FitBoxToText','on')
title('Histogram for all I_x(n,f), I_y(n,f), I_z(n,f) (free-space)')
xlabel('Intensity')
ylabel('Number of values')

subplot(2,2,2);
histogram(RGB_room, N_bins);
line(mean(RGB_room) + 2*std(RGB_room)*[1 1],[0 200000],'LineStyle','--')
line(mean(RGB_room) - 2*std(RGB_room)*[1 1],[0 200000],'LineStyle','--')
text(mean(RGB_room) - 2*std(RGB_room), 0.1*10^5, '\mu-2\sigma', 'HorizontalAlignment','right')
text(mean(RGB_room) + 2*std(RGB_room), 0.1*10^5, '\mu+2\sigma', 'HorizontalAlignment','left')
info = {['mean \mu: ' num2str(mean(RGB_room), '%.2e')], ...
        ['standard deviation \sigma: ' num2str(std(RGB_room), '%.2e')], ...
        ['max: ' num2str(max(RGB_room))], ... 
        ['min: ' num2str(min(RGB_room))]};
annotation('textbox', [0.75 0.9 0 0], 'String', info, 'FitBoxToText','on')
title('Histogram for all I_x(n,f), I_y(n,f), I_z(n,f) (room)')
xlabel('Intensity')
ylabel('Number of values')

subplot(2,2,3);
histogram(alpha_free, N_bins);
line(mean(alpha_free) + 2*std(alpha_free)*[1 1],[0 50000],'LineStyle','--')
line(mean(alpha_free) - 2*std(alpha_free)*[1 1],[0 50000],'LineStyle','--')
text(mean(alpha_free) - 2*std(alpha_free), 0.2*10^4, '\mu-2\sigma', 'HorizontalAlignment','right')
text(mean(alpha_free) + 2*std(alpha_free), 0.2*10^4, '\mu+2\sigma', 'HorizontalAlignment','left')
info = {['mean \mu: ' num2str(mean(alpha_free), '%.2e')], ...
        ['standard deviation \sigma: ' num2str(std(alpha_free), '%.2e')], ...
        ['max: ' num2str(max(alpha_free))], ... 
        ['min: ' num2str(min(alpha_free))]};
annotation('textbox', [0.31 0.4 0 0], 'String', info, 'FitBoxToText','on')
title('Histogram for all a_{00}(n,f) (free-space)')
xlabel('Intensity')
ylabel('Number of values')

subplot(2,2,4);
histogram(alpha_room, N_bins);
line(mean(alpha_room) + 2*std(alpha_room)*[1 1],[0 50000],'LineStyle','--')
line(mean(alpha_room) - 2*std(alpha_room)*[1 1],[0 50000],'LineStyle','--')
text(mean(alpha_room) - 2*std(alpha_room), 0.2*10^4, '\mu-2\sigma', 'HorizontalAlignment','right')
text(mean(alpha_room) + 2*std(alpha_room), 0.2*10^4, '\mu+2\sigma', 'HorizontalAlignment','left')
info = {['mean \mu: ' num2str(mean(alpha_room), '%.2e')], ...
        ['standard deviation \sigma: ' num2str(std(alpha_room), '%.2e')], ...
        ['max: ' num2str(max(alpha_room))], ... 
        ['min: ' num2str(min(alpha_room))]};
annotation('textbox', [0.75 0.4 0 0], 'String', info, 'FitBoxToText','on')
title('Histogram for all a_{00}(n,f) (room)')
xlabel('Intensity')
ylabel('Number of values')