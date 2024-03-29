import plotly.express as px
from modules.utils import clean_data, split_data, get_roc_curve, get_confusion_matrix

# class
class Plot:
    def __init__(self, data):
        self.data = data
        self.df = clean_data(data)
        self.X_train, self.X_test, self.y_train, self.y_test = split_data(self.df)
        
    def plot_pie(self):
        object_columns = self.data.select_dtypes(include=['object']).columns
        # get the columns with type non object
        non_object_columns = self.data.select_dtypes(exclude=['object']).columns
        labels = ["Qualitatif", "Quantitatif"]
        data = [object_columns.size, non_object_columns.size]
        # plot the number of quantitatif and qualitatif columns using plotly.express
        fig = px.pie(values=data, names=labels, title='Number of Quantitatif and Qualitatif columns')
        fig.update_layout(
            width=700,  # Adjust the width as needed
            height=500,  # Adjust the height as needed
            legend=dict(
                x=0.0,  # Adjust the x position of the legend (0.5 is centered)
                y=1.1   # Adjust the y position of the legend (increase to bring it closer)
            )
        )
        return fig

    def plot_correlation_matrix(self):
        # plot the correlation matrix using plotly.express
        fig = px.imshow(self.df.corr(), title='Correlation matrix')
        fig.update_layout(
            width=600,  # Adjust the width as needed
            height=500,  # Adjust the height as needed
            legend=dict(
                x=0.5,  # Adjust the x position of the legend (0.5 is centered)
                y=1.1   # Adjust the y position of the legend (increase to bring it closer)
            )
        )
        return fig
    
    def plot_confusion_matrix(self, model):
        confusion_matrix = get_confusion_matrix(model)
        fig = px.imshow(confusion_matrix, title='Confusion matrix')
        for i in range(len(confusion_matrix)):
            for j in range(len(confusion_matrix[i])):
                fig.add_annotation(
                    x=j,
                    y=i,
                    text=str(confusion_matrix[i, j]),
                    showarrow=False,
                    font=dict(color='black')
                )
        fig.update_layout(
            width=600,  # Adjust the width as needed
            height=500,  # Adjust the height as needed
            legend=dict(
                x=0.5,  # Adjust the x position of the legend (0.5 is centered)
                y=1.1   # Adjust the y position of the legend (increase to bring it closer)
            )
        )
        return fig

    def plot_roc_curve(self, model):
        fpr, tpr, _, auc_score =get_roc_curve(model)
        fig = px.area(
            x=fpr, y=tpr,
            title=f'ROC Curve (AUC={auc_score:.4f})',
            labels=dict(x='False Positive Rate', y='True Positive Rate'),
            width=700,  # Adjust the width as needed
            height=500,  # Adjust the height as needed
        )
        fig.add_shape(
            type='line', line=dict(dash='dash'),
            x0=0, x1=1, y0=0, y1=1
        )
        return fig

    def get_plot(self, plot_name, x = None, y = None):
        if plot_name == "quantitatif_qualitatif_pie":
            return self.plot_pie()
        
        elif plot_name == "correlation_matrix":
            return self.plot_correlation_matrix()

        elif plot_name == "scatter":
            return px.scatter(self.df, x=x, y=y, title=f"{x} vs {y}")
        
        elif plot_name == "line":
            return px.line(self.df, x=x, y=y, title=f"{x} vs {y}")
        
        elif plot_name == "bar":
            return px.bar(self.df, x=x, y=y, title=f"{x} vs {y}")


        return None


