function [fig2] = plot_correlation_analysis(t, happiness_scale, social_activity)
    happiness_scale(happiness_scale < 0) = 0;
    happiness_scale(happiness_scale > 10) = 10;

    n = length(t);

    fig1 = figure;
    subplot(2, 1, 1);
    plot(t, happiness_scale, 'b');
    title('Happiness Scale (Bounded between 0 and 10)');
    xlabel('Time');
    ylabel('Happiness Scale');

    subplot(2, 1, 2);
    stem(t, social_activity, 'r');  
    title('Social Activity');
    xlabel('Time');
    ylabel('Social Activity (0 or 1)');

    autocorr_happiness = xcorr(happiness_scale, 'coeff');
    lags = -(n - 1):(n - 1); 

    [peak_autocorr, locs_autocorr] = findpeaks(autocorr_happiness, 'MinPeakProminence', 0.1);  
    peak_lags_autocorr = lags(locs_autocorr);  

    disp('Significant peak values for autocorrelation of happiness_scale:');
    disp(table(peak_lags_autocorr', peak_autocorr', 'VariableNames', {'Lag', 'PeakValue'}));

    fig2 = figure;
    subplot(2, 1, 1);
    plot(lags, autocorr_happiness, 'b');
    hold on;
    plot(peak_lags_autocorr, peak_autocorr, 'ro', 'MarkerFaceColor', 'r'); 
    title('Autocorrelation of Happiness Scale');
    xlabel('Lags');
    ylabel('Autocorrelation');
    hold off;

    crosscorr_happiness_social = xcorr(happiness_scale, social_activity, 'coeff');

    [peak_crosscorr, locs_crosscorr] = findpeaks(crosscorr_happiness_social, 'MinPeakProminence', 0.1); 
    peak_lags_crosscorr = lags(locs_crosscorr);  

    disp('Significant peak values for cross-correlation between happiness_scale and social_activity:');
    disp(table(peak_lags_crosscorr', peak_crosscorr', 'VariableNames', {'Lag', 'PeakValue'}));

    subplot(2, 1, 2);
    plot(lags, crosscorr_happiness_social, 'r');
    hold on;
    plot(peak_lags_crosscorr, peak_crosscorr, 'ro', 'MarkerFaceColor', 'r');
    title('Cross-Correlation between Happiness Scale and Social Activity');
    xlabel('Lags');
    ylabel('Cross-Correlation');
    hold off;
end
