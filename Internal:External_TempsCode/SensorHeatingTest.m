%% Set File Names and Parameters
dataFile = 'HeatLossTest.xlsx'; % Combined data file
sheetname_gun = 'Gun_Data'; % Sheet name for gun data
sheetname_sensor = 'Sensor_Data'; % Sheet name for sensor data

%% Import and Process Heat Gun Data
% Import heat gun data from the specified sheet
data_gun = readtable(dataFile, 'Sheet', sheetname_gun, 'ReadVariableNames', true);
time_gun = data_gun{:, 1}; % Column for times in minutes
temps_gun = data_gun{:, 2:12}; % Columns for temperature measurements

% Average temperature across heat gun points
avg_temp_gun_points = mean(temps_gun, 2, 'omitnan');

%% Import and Process Temperature Sensor Data
% Import raw sensor data strings
data_sensor = readtable(dataFile, 'Sheet', sheetname_sensor, 'ReadVariableNames', false, 'ExpectedNumVariables', 1);
sensor_data_raw = data_sensor{:, 1};

temperatures_celsius = []; % Initialize array for valid temperatures
sensor_times_seconds = []; % Initialize array for timestamps of valid temperatures
current_time_seconds = 0;
sensor_interval_seconds = 2;

fprintf('Processing sensor data. Assuming each line (temp or error) represents a %.f second interval.\n', sensor_interval_seconds);

% Process each line from the sensor data
for i = 1:length(sensor_data_raw)
    rowText = sensor_data_raw{i};
    if ischar(rowText) || isstring(rowText)
        if startsWith(rowText, 'Temp:')
            tokens = regexp(rowText, 'Temp: [\d\.]+ F / ([\d\.]+) C', 'tokens');
            if ~isempty(tokens) && ~isempty(tokens{1})
                try
                    temperature_celsius = str2double(tokens{1});
                    % Store ALL valid temperatures and their times initially
                    temperatures_celsius = [temperatures_celsius; temperature_celsius];
                    sensor_times_seconds = [sensor_times_seconds; current_time_seconds];
                catch ME
                    fprintf('Warning: Could not convert parsed temperature "%s" to double on line %d. Skipping. Error: %s\n', tokens{1}, i, ME.message);
                end
            else
                 fprintf('Warning: Found "Temp:" but could not parse format on line %d: "%s". Skipping temperature.\n', i, rowText);
            end
        end
    else
         fprintf('Warning: Non-text data found on line %d. Skipping.\n', i);
    end
    % Increment time AFTER processing the current line
    current_time_seconds = current_time_seconds + sensor_interval_seconds;
end

% --- Modification: Ignore the first valid data point collected ---
if ~isempty(temperatures_celsius)
    fprintf('Collected %d valid sensor data points initially.\n', length(temperatures_celsius));
    if length(temperatures_celsius) >= 1
        fprintf('Ignoring the first valid sensor data point (Temp: %.1f C at %.1f s).\n', temperatures_celsius(1), sensor_times_seconds(1));
        temperatures_celsius = temperatures_celsius(2:end);
        sensor_times_seconds = sensor_times_seconds(2:end);
    end
else
     warning('No valid sensor temperature data points found to process or ignore.');
end
% --- End Modification ---

fprintf('Using %d valid sensor temperature points for analysis.\n', length(temperatures_celsius));

% Convert the timestamps for the remaining readings to relative minutes
relative_minutes = sensor_times_seconds / 60;

% Check if any sensor data remains
if isempty(relative_minutes) && isempty(temperatures_celsius) && length(sensor_data_raw)>0 % Check if raw data existed
   warning('No sensor data points remaining after processing and ignoring the first point. Cannot perform alignment or regression.');
   can_proceed = false;
else
   can_proceed = true; % Okay to proceed
end

%% Plotting All Points Together (Time Series)
figure;
hold on;
plot(time_gun, temps_gun, '-');
plot(time_gun, avg_temp_gun_points, 'k--', 'LineWidth', 2, 'DisplayName', 'Average Gun Temp');

if can_proceed % Only plot sensor data if it exists
    plot(relative_minutes, temperatures_celsius, 'r-o', 'LineWidth', 1.5, 'MarkerSize', 4, 'DisplayName', 'Sensor Temperature');
    sensor_legend_entry = {'Sensor Temperature'};
else
    sensor_legend_entry = {};
end

xlabel('Time (minutes)');
ylabel('Temperature (°C)');
title('Temperature Measurements: Heat Gun vs Sensor (Time Series)');
gun_legends = cell(1, size(temps_gun, 2));
for i = 1:size(temps_gun, 2)
    gun_legends{i} = sprintf('Gun Point %d', i);
end
legend([gun_legends, {'Average Gun Temp'}, sensor_legend_entry], 'Location', 'best');
grid on;
hold off;

%% Data Alignment for Regression Analysis
% Initialize regression_possible flag
regression_possible = false; 
interp_sensor_temps = []; % Initialize to avoid errors if not calculated

if can_proceed && length(relative_minutes) > 1 % Need at least 2 points to interpolate
    fprintf('\nInterpolating sensor data onto gun data time points...\n');
    interp_sensor_temps = interp1(relative_minutes, temperatures_celsius, time_gun, 'linear', 'extrap');
    fprintf('Interpolation complete.\n');
    
    % Optional: Calculate differences (MAE, RMSE, Bias) if desired
    temperature_differences = avg_temp_gun_points - interp_sensor_temps;
    mae = mean(abs(temperature_differences), 'omitnan');
    rmse = sqrt(mean(temperature_differences.^2, 'omitnan'));
    bias = mean(temperature_differences, 'omitnan');
    fprintf('Comparison Metrics (Average Gun Temp - Interpolated Sensor Temp):\n');
    fprintf('  MAE: %.2f C, RMSE: %.2f C, Bias: %.2f C\n', mae, rmse, bias);
    
    regression_possible = true; % Flag that we can proceed to regression

elseif can_proceed % We have sensor data, but not enough for interpolation
    warning('Not enough unique sensor data points (%d) remaining for interpolation. Skipping regression.', length(relative_minutes));
    regression_possible = false;
else % No sensor data from the start
    regression_possible = false; % Cannot do regression
end

%% Develop Mapping Equation (Regression Analysis)
if regression_possible % Check if interpolation was successful

    fprintf('\n--- Developing Temperature Mapping Equation ---\n');

    % Prepare data for regression:
    X_internal = interp_sensor_temps; % Use the interpolated sensor data
    Y_external = avg_temp_gun_points; % Use the average gun data

    % Remove any NaN values which would interfere with fitting
    valid_indices = ~isnan(X_internal) & ~isnan(Y_external);
    X_fit = X_internal(valid_indices);
    Y_fit = Y_external(valid_indices);

    if length(X_fit) < 2
        warning('Not enough valid, overlapping data points after interpolation for regression analysis.');
    else
        fprintf('Using %d valid data points for regression.\n', length(X_fit));

        % Initialize results storage
        models = {'Linear', 'Quadratic', 'PowerLaw'};
        rsq_values = [-Inf, -Inf, -Inf]; % Default to invalid fit
        rmse_values = [Inf, Inf, Inf];
        equations = {'', '', ''};
        model_objects = {[], [], []}; % To store model results like mdl_linear etc.
        coeffs = {[], [], []};

        % --- Fit Linear Model ---
        try
            mdl_linear = fitlm(X_fit, Y_fit);
            model_objects{1} = mdl_linear;
            disp('Linear Model Summary (ExternalTemp ~ 1 + InternalTemp):');
            disp(mdl_linear);
            coeffs_linear = mdl_linear.Coefficients.Estimate;
            coeffs{1} = coeffs_linear;
            p2_intercept = coeffs_linear(1);
            p1_slope = coeffs_linear(2);
            equations{1} = sprintf('ExternalTemp = %.4f * InternalTemp + %.4f', p1_slope, p2_intercept);
            rsq_values(1) = mdl_linear.Rsquared.Ordinary;
            rmse_values(1) = mdl_linear.RMSE;
            fprintf('\nLinear Equation:\n  %s\n', equations{1});
            fprintf('  R-squared: %.4f, RMSE: %.4f C\n', rsq_values(1), rmse_values(1));
        catch ME_lin
             fprintf('Skipping linear model results.\n');
        end
        
        fprintf(sprintf('\n--------------------------------------------------'));

        % --- Fit Quadratic Model ---
         try
            mdl_poly2 = fitlm(X_fit, Y_fit, 'poly2');
            model_objects{2} = mdl_poly2;
            fprintf('\nQuadratic Model Summary (ExternalTemp ~ 1 + InternalTemp + InternalTemp^2):\n');
            disp(mdl_poly2);
            coeffs_poly2 = mdl_poly2.Coefficients.Estimate;
            coeffs{2} = coeffs_poly2;
            p3_poly_intercept = coeffs_poly2(1);
            p2_poly_linear = coeffs_poly2(2);
            p1_poly_quadratic = coeffs_poly2(3);
            equations{2} = sprintf('ExternalTemp = %.4f * InternalTemp^2 + %.4f * InternalTemp + %.4f', ...
                 p1_poly_quadratic, p2_poly_linear, p3_poly_intercept);
            rsq_values(2) = mdl_poly2.Rsquared.Ordinary;
            rmse_values(2) = mdl_poly2.RMSE;
            fprintf('\nQuadratic Equation:\n  %s\n', equations{2});
            fprintf('  R-squared: %.4f, RMSE: %.4f C\n', rsq_values(2), rmse_values(2));
        catch ME_quad
             fprintf('Skipping quadratic model results.\n');
        end
        
        fprintf(sprintf('\n--------------------------------------------------'));

        % --- Fit Non-Linear Model (Power Law: y = a*x^b + c) ---
        fprintf('\nFitting Non-Linear Model (Power Law: ExternalTemp = a*InternalTemp^b + c)\n');
        model_func_power = @(beta, x) beta(1) * x.^beta(2) + beta(3); % beta(1)=a, beta(2)=b, beta(3)=c
        
        % Initial guesses (can be critical for NLM)
        % Rough estimate based on data range
        c_guess = min(Y_fit) - 0.1*abs(min(Y_fit)); % Start slightly below min Y
        b_guess = 1; % Start assuming roughly linear power initially
        a_guess = (max(Y_fit)-c_guess) / (max(X_fit)^b_guess); % Rough scaling factor
        if ~isfinite(a_guess) || a_guess == 0, a_guess = 1; end % Safety check
        if ~isfinite(c_guess), c_guess = 0; end % Safety check

        beta0 = [abs(a_guess), b_guess, c_guess]; % Ensure 'a' guess is positive if expected
        fprintf('Using initial guesses for Power Law: a=%.3f, b=%.3f, c=%.3f\n', beta0(1), beta0(2), beta0(3));

        try
            opts = statset('TolFun', 1e-8, 'TolX', 1e-8, 'MaxIter', 500, 'Display', 'off');
            mdl_nlm = fitnlm(X_fit, Y_fit, model_func_power, beta0, 'Options', opts);
            model_objects{3} = mdl_nlm;
            disp('Non-Linear Power Law Model Summary:');
            disp(mdl_nlm);
            coeffs_nlm = mdl_nlm.Coefficients.Estimate; % [a, b, c]
            coeffs{3} = coeffs_nlm;
            
            % Calculate R-squared manually for NLM
            SSE_nlm = sum(mdl_nlm.Residuals.Raw.^2);
            SST_nlm = sum((Y_fit - mean(Y_fit)).^2);
            if SST_nlm == 0 
               rsq_calc_nlm = 1; % Perfect fit if Y is constant
            else
               rsq_calc_nlm = 1 - SSE_nlm / SST_nlm;
            end
             % Check if R-squared is valid (can be negative if model is worse than mean)
             if rsq_calc_nlm < 0 
                 warning('Non-linear model R-squared is negative (%.4f), indicating poor fit. Treating as 0 for comparison.', rsq_calc_nlm);
                 rsq_calc_nlm = 0;
             end
            rsq_values(3) = rsq_calc_nlm;
            rmse_values(3) = mdl_nlm.RMSE;

            equations{3} = sprintf('ExternalTemp = %.4f * InternalTemp ^ (%.4f) + %.4f', coeffs_nlm(1), coeffs_nlm(2), coeffs_nlm(3));
            fprintf('\nNon-Linear Power Law Equation:\n  %s\n', equations{3});
            fprintf('  R-squared (calculated): %.4f, RMSE: %.4f C\n', rsq_values(3), rmse_values(3));

        catch ME_nlm
            fprintf('Skipping non-linear model results.\n');
            % Results remain at default invalid values
        end
        fprintf(sprintf('--------------------------------------------------\n'));

        % --- Visualization (Regression Fit) ---
        figure;
        plot(X_fit, Y_fit, 'bo', 'DisplayName', 'Actual Data Points (Aligned)');
        hold on;
        X_plot = linspace(min(X_fit), max(X_fit), 100)';
        
        plot_legends = {'Actual Data Points (Aligned)'}; % Start legend cell array

        % Plot Linear Fit (if successful)
        if ~isempty(model_objects{1})
            plot(X_plot, predict(model_objects{1}, X_plot), 'r-', 'LineWidth', 1.5);
            plot_legends{end+1} = sprintf('Linear (R^2=%.3f)', rsq_values(1));
        end
        % Plot Quadratic Fit (if successful)
         if ~isempty(model_objects{2})
            plot(X_plot, predict(model_objects{2}, X_plot), 'g--', 'LineWidth', 1.5);
             plot_legends{end+1} = sprintf('Quadratic (R^2=%.3f)', rsq_values(2));
         end
        % Plot Non-Linear Fit (if successful)
        if ~isempty(model_objects{3})
            plot(X_plot, predict(model_objects{3}, X_plot), 'm:', 'LineWidth', 2);
             plot_legends{end+1} = sprintf('Power Law (R^2=%.3f)', rsq_values(3));
        end

        xlabel('Internal Sensor Temperature (°C) (Interpolated)');
        ylabel('Average External Gun Temperature (°C)');
        title('Mapping Internal Sensor Temp to External Mattress Temp (Regression)');
        legend(plot_legends, 'Location', 'best'); % Use dynamic legend
        grid on;
        hold off;

        % --- Recommendation ---
        fprintf('\nRecommendation:\n');
        fprintf(' - Examine R-squared, RMSE, and the plot for all fitted models.\n');

        % Find best R-squared among valid fits
        valid_fits = isfinite(rsq_values) & rsq_values >= 0; % Indices of models that ran without error and have non-negative R^2
        if ~any(valid_fits)
             fprintf(' - No models fitted successfully.\n');
        else
            valid_rsq = rsq_values(valid_fits);
            valid_models_idx = find(valid_fits); % Get original indices (1, 2, or 3)
            
            [best_rsq, temp_idx] = max(valid_rsq); % Find max R^2 among valid ones
            best_model_idx = valid_models_idx(temp_idx); % Get original index of best model
            
            fprintf(' - Best R-squared (%.4f) achieved by %s model.\n', best_rsq, models{best_model_idx});

            % Simplicity tolerance - prefer simpler model if R^2 is close
            tolerance = 0.01; 
            
            chosen_model_idx = best_model_idx; % Start with the best R^2 model

            % Check if a simpler model is within tolerance
            % Check Quadratic vs PowerLaw (if PowerLaw was best)
            if best_model_idx == 3 && valid_fits(2) && (rsq_values(2) >= best_rsq - tolerance)
                chosen_model_idx = 2;
                fprintf(' - Quadratic R^2 (%.4f) is within tolerance (%.2f) of Power Law, preferring Quadratic.\n', rsq_values(2), tolerance);
            end
            % Check Linear vs chosen (Quadratic or PowerLaw)
            if chosen_model_idx > 1 && valid_fits(1) && (rsq_values(1) >= rsq_values(chosen_model_idx) - tolerance)
                 chosen_model_idx = 1;
                 fprintf(' - Linear R^2 (%.4f) is within tolerance (%.2f) of %s, preferring Linear.\n', rsq_values(1), tolerance, models{best_model_idx});
            end

            fprintf(' - Recommended Model: %s\n', models{chosen_model_idx});

            % Print the recommended equation
            if ~isempty(equations{chosen_model_idx})
                 fprintf(' - Recommended Equation:\n     %s\n', equations{chosen_model_idx});
            else
                 fprintf(' - Could not retrieve equation for recommended model.\n');
            end

            fprintf(' - Ensure the equation is used within the tested temperature range (approx. %.1f C to %.1f C internal).\n', min(X_fit), max(X_fit));
        end % end check if any valid fits

    end % end check for enough regression points
else
     fprintf('\nSkipping regression analysis because data alignment was not possible or yielded too few points.\n');
end % end check if regression is possible

% --- End of Script ---